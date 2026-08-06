import base64
import json
import os
import re
from typing import Any, Dict, Optional, Tuple

import psycopg
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

APP_VERSION = "NDSP_CURRENT_USER_DISPLAY_DB_FINAL"
DB_DSN = os.getenv("NDSP_AUTH_DB_DSN", "dbname=ndsp_auth user=postgres")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", re.I)

app = FastAPI(title="NDSP Current User Display API", version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://my.ndsp.app",
        "https://ndsp.app",
        "https://www.ndsp.app",
    ],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


def clean(v: Any) -> str:
    return str(v or "").strip()


def valid_email(v: Any) -> str:
    v = clean(v)
    return v if EMAIL_RE.match(v) else ""


def b64url_decode(raw: str) -> str:
    raw = raw.replace("-", "+").replace("_", "/")
    raw += "=" * (-len(raw) % 4)
    return base64.b64decode(raw.encode()).decode("utf-8", "ignore")


def email_from_obj(obj: Any) -> str:
    if not isinstance(obj, dict):
        return ""

    for key in (
        "email",
        "user_email",
        "email_address",
        "username",
        "login",
        "sub",
    ):
        e = valid_email(obj.get(key))
        if e:
            return e

    for key in ("user", "account", "profile", "data", "session"):
        e = email_from_obj(obj.get(key))
        if e:
            return e

    return ""


def email_from_token(value: str) -> str:
    value = clean(value)
    if value.count(".") < 2:
        return ""

    try:
        payload = json.loads(b64url_decode(value.split(".")[1]))
        return email_from_obj(payload)
    except Exception:
        return ""


def email_from_any_value(value: str) -> str:
    value = clean(value)

    e = valid_email(value)
    if e:
        return e

    e = email_from_token(value)
    if e:
        return e

    try:
        return email_from_obj(json.loads(value))
    except Exception:
        return ""


def extract_email(request: Request, email_query: Optional[str]) -> str:
    # 1) البريد المرسل من الواجهة بعد قراءته من جلسة الدخول.
    e = valid_email(email_query)
    if e:
        return e

    # 2) Authorization Bearer JWT.
    auth = clean(request.headers.get("authorization"))
    if auth.lower().startswith("bearer "):
        e = email_from_token(auth.split(" ", 1)[1])
        if e:
            return e

    # 3) Cookies.
    for _, value in request.cookies.items():
        e = email_from_any_value(value)
        if e:
            return e

    return ""


def get_conn():
    return psycopg.connect(DB_DSN)


def list_user_tables(conn) -> list[Tuple[str, str, list[str]]]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT table_schema, table_name, array_agg(column_name ORDER BY ordinal_position) AS cols
            FROM information_schema.columns
            WHERE table_schema NOT IN ('pg_catalog','information_schema')
            GROUP BY table_schema, table_name
            HAVING bool_or(lower(column_name) IN ('email','user_email','email_address','login_email'))
            ORDER BY
              CASE
                WHEN table_name='users' THEN 1
                WHEN table_name LIKE '%user%' THEN 2
                WHEN table_name LIKE '%trial%' THEN 3
                ELSE 9
              END,
              table_schema,
              table_name
            """
        )
        return [(r[0], r[1], list(r[2])) for r in cur.fetchall()]


def choose_columns(cols: list[str]) -> Dict[str, Any]:
    lower_map = {c.lower(): c for c in cols}

    email_col = None
    for c in ("email", "user_email", "email_address", "login_email"):
        if c in lower_map:
            email_col = lower_map[c]
            break

    name_cols = []
    for c in (
        "username",
        "display_name",
        "full_name",
        "name",
        "first_name",
        "last_name",
        "email",
    ):
        if c in lower_map:
            name_cols.append(lower_map[c])

    id_col = None
    for c in ("id", "user_id", "uuid"):
        if c in lower_map:
            id_col = lower_map[c]
            break

    return {
        "email_col": email_col,
        "name_cols": name_cols,
        "id_col": id_col,
    }


def quote_ident(x: str) -> str:
    return '"' + x.replace('"', '""') + '"'



def find_user_direct_public_users(email: str) -> Dict[str, Any]:
    email = valid_email(email)
    if not email:
        return {}

    sql = """
        SELECT
            id,
            name,
            email,
            canonical_email
        FROM public.users
        WHERE lower(email) = lower(%s)
           OR lower(canonical_email) = lower(%s)
        ORDER BY created_at DESC NULLS LAST
        LIMIT 1
    """

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (email, email))
                row = cur.fetchone()
                if not row:
                    return {}

                user_id, name, db_email, canonical_email = row
                display_name = clean(name) or clean(db_email) or clean(canonical_email) or email

                return {
                    "found": True,
                    "schema": "public",
                    "table": "users",
                    "id": str(user_id),
                    "email": clean(db_email) or email,
                    "canonical_email": clean(canonical_email),
                    "display_name": display_name,
                    "source": "database_public_users_direct",
                }
    except Exception as e:
        return {
            "found": False,
            "email": email,
            "display_name": email,
            "source": "direct_public_users_error",
            "error": str(e),
        }



def find_user_by_email(email: str) -> Dict[str, Any]:
    email = valid_email(email)
    if not email:
        return {}

    direct = find_user_direct_public_users(email)
    if direct.get("found"):
        return direct

    with get_conn() as conn:
        tables = list_user_tables(conn)

        for schema, table, cols in tables:
            selected = choose_columns(cols)
            email_col = selected["email_col"]
            name_cols = selected["name_cols"]
            id_col = selected["id_col"]

            if not email_col:
                continue

            select_cols = []
            if id_col:
                select_cols.append(id_col)

            for c in name_cols:
                if c not in select_cols:
                    select_cols.append(c)

            if email_col not in select_cols:
                select_cols.append(email_col)

            select_sql = ", ".join(quote_ident(c) for c in select_cols)
            sql = (
                f"SELECT {select_sql} "
                f"FROM {quote_ident(schema)}.{quote_ident(table)} "
                f"WHERE lower({quote_ident(email_col)}) = lower(%s) "
                f"LIMIT 1"
            )

            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (email,))
                    row = cur.fetchone()
                    if not row:
                        continue

                    data = dict(zip(select_cols, row))

                    display_name = ""
                    first = clean(data.get("first_name"))
                    last = clean(data.get("last_name"))
                    if first or last:
                        display_name = clean(f"{first} {last}")

                    if not display_name:
                        for c in (
                            "username",
                            "display_name",
                            "full_name",
                            "name",
                        ):
                            for actual in data.keys():
                                if actual.lower() == c:
                                    candidate = clean(data.get(actual))
                                    if candidate and not valid_email(candidate):
                                        display_name = candidate
                                        break
                            if display_name:
                                break

                    if not display_name:
                        display_name = email

                    return {
                        "found": True,
                        "schema": schema,
                        "table": table,
                        "email": email,
                        "display_name": display_name,
                        "source": "database",
                    }

            except Exception:
                continue

    return {
        "found": False,
        "email": email,
        "display_name": email,
        "source": "fallback_email",
    }


@app.get("/api/account/me-display/health")
def health():
    return {
        "ok": True,
        "service": APP_VERSION,
        "database": "ndsp_auth",
        "read_only": True,
    }


@app.get("/api/account/me-display")
def me_display(request: Request, email: Optional[str] = Query(default=None)):
    resolved_email = extract_email(request, email)

    if not resolved_email:
        return JSONResponse(
            {
                "ok": False,
                "service": APP_VERSION,
                "reason": "EMAIL_NOT_FOUND_IN_SESSION",
            },
            status_code=200,
        )

    user = find_user_by_email(resolved_email)

    return {
        "ok": True,
        "service": APP_VERSION,
        "email": resolved_email,
        "display_name": user.get("display_name") or resolved_email,
        "found": bool(user.get("found")),
        "source": user.get("source"),
        "table": user.get("table"),
    }
