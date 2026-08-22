import os
import re
from typing import Optional, Tuple

import psycopg
from psycopg import sql
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from passlib.context import CryptContext

APP_VERSION = "NDSP_CHANGE_PASSWORD_GATEWAY_FINAL"
DATABASE_URL = os.getenv("DATABASE_URL", "dbname=ndsp_auth user=postgres")

pwd_context = CryptContext(
    schemes=["bcrypt", "pbkdf2_sha256", "django_pbkdf2_sha256"],
    deprecated="auto"
)

app = FastAPI(title="NDSP Change Password Gateway", version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://my.ndsp.app",
        "https://api.ndsp.app",
        "https://ndsp.app",
    ],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

class ChangePasswordPayload(BaseModel):
    email: str = Field(..., min_length=3, max_length=254)
    current_password: str = Field(..., min_length=1, max_length=512)
    new_password: str = Field(..., min_length=8, max_length=512)
    confirm_password: Optional[str] = Field(None, max_length=512)

def clean_email(v: str) -> str:
    return (v or "").strip().lower()

def valid_email(v: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v or ""))

def validate_new_password(pw: str) -> Optional[str]:
    if len(pw or "") < 8:
        return "NEW_PASSWORD_MIN_8"
    if len(pw) > 128:
        return "NEW_PASSWORD_TOO_LONG"
    if not re.search(r"[A-Za-z]", pw) or not re.search(r"\d", pw):
        return "NEW_PASSWORD_MUST_INCLUDE_LETTER_AND_NUMBER"
    return None

def get_conn():
    return psycopg.connect(DATABASE_URL)

def table_columns(conn, schema: str, table: str):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema=%s AND table_name=%s
            """,
            (schema, table),
        )
        return {r[0] for r in cur.fetchall()}

def discover_user_tables(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema NOT IN ('pg_catalog','information_schema')
              AND table_type='BASE TABLE'
            ORDER BY
              CASE
                WHEN table_name='users' THEN 0
                WHEN table_name ILIKE '%user%' THEN 1
                WHEN table_name ILIKE '%credential%' THEN 2
                ELSE 9
              END,
              table_schema,
              table_name
            """
        )
        return cur.fetchall()

def find_user_record(conn, email: str):
    email_cols = ["email", "user_email", "email_address", "login_email"]
    hash_cols = ["password_hash", "hashed_password", "password_digest", "password", "password_bcrypt", "hash"]

    for schema, table in discover_user_tables(conn):
        cols = table_columns(conn, schema, table)
        ecols = [c for c in email_cols if c in cols]
        hcols = [c for c in hash_cols if c in cols]
        if not ecols or not hcols:
            continue

        email_col = ecols[0]
        hash_col = hcols[0]

        with conn.cursor() as cur:
            q = sql.SQL("SELECT {email_col}, {hash_col} FROM {tbl} WHERE lower({email_col}) = lower(%s) LIMIT 1").format(
                email_col=sql.Identifier(email_col),
                hash_col=sql.Identifier(hash_col),
                tbl=sql.Identifier(schema, table),
            )
            cur.execute(q, (email,))
            row = cur.fetchone()
            if row:
                return schema, table, email_col, hash_col, row[1]

    return None

def verify_password(current_password: str, stored_hash: str) -> bool:
    if not stored_hash:
        return False

    stored_hash = str(stored_hash)

    try:
        if stored_hash.startswith("$") or stored_hash.startswith("pbkdf2_"):
            return bool(pwd_context.verify(current_password, stored_hash))
    except Exception:
        pass

    # Fallback only for old/plain deployments, then it upgrades to bcrypt.
    return stored_hash == current_password

def update_password(conn, schema: str, table: str, email_col: str, hash_col: str, email: str, new_password: str):
    new_hash = pwd_context.hash(new_password)

    cols = table_columns(conn, schema, table)
    nullable_updates = []
    for c in ["reset_token", "password_reset_token", "reset_password_token", "reset_expires", "reset_token_expires_at", "password_reset_expires_at"]:
        if c in cols:
            nullable_updates.append(c)

    set_parts = [sql.SQL("{} = %s").format(sql.Identifier(hash_col))]
    values = [new_hash]

    for c in nullable_updates:
        set_parts.append(sql.SQL("{} = NULL").format(sql.Identifier(c)))

    q = sql.SQL("UPDATE {tbl} SET {sets} WHERE lower({email_col}) = lower(%s)").format(
        tbl=sql.Identifier(schema, table),
        sets=sql.SQL(", ").join(set_parts),
        email_col=sql.Identifier(email_col),
    )
    values.append(email)

    with conn.cursor() as cur:
        cur.execute(q, values)
        return cur.rowcount

@app.get("/api/account/change-password/health")
async def health():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return {"ok": True, "service": APP_VERSION, "database": "ok"}
    except Exception as e:
        return {"ok": False, "service": APP_VERSION, "database": "error", "error": str(e)[:180]}

@app.post("/api/account/change-password")
async def change_password(payload: ChangePasswordPayload, request: Request):
    email = clean_email(payload.email)

    if not valid_email(email):
        return {"ok": False, "code": "EMAIL_INVALID", "message_ar": "البريد الإلكتروني غير صحيح."}

    if payload.confirm_password is not None and payload.new_password != payload.confirm_password:
        return {"ok": False, "code": "PASSWORD_CONFIRM_MISMATCH", "message_ar": "تأكيد كلمة المرور غير مطابق."}

    pw_error = validate_new_password(payload.new_password)
    if pw_error:
        return {"ok": False, "code": pw_error, "message_ar": "كلمة المرور الجديدة يجب أن تكون 8 أحرف على الأقل وتحتوي حرفًا ورقمًا."}

    if payload.current_password == payload.new_password:
        return {"ok": False, "code": "NEW_PASSWORD_SAME_AS_OLD", "message_ar": "كلمة المرور الجديدة يجب أن تختلف عن الحالية."}

    try:
        with get_conn() as conn:
            rec = find_user_record(conn, email)
            if not rec:
                return {"ok": False, "code": "USER_NOT_FOUND", "message_ar": "لم يتم العثور على الحساب."}

            schema, table, email_col, hash_col, stored_hash = rec

            if not verify_password(payload.current_password, stored_hash):
                return {"ok": False, "code": "CURRENT_PASSWORD_INVALID", "message_ar": "كلمة المرور الحالية غير صحيحة."}

            rowcount = update_password(conn, schema, table, email_col, hash_col, email, payload.new_password)
            conn.commit()

            if rowcount < 1:
                return {"ok": False, "code": "PASSWORD_UPDATE_FAILED", "message_ar": "تعذر تحديث كلمة المرور."}

            return {
                "ok": True,
                "code": "PASSWORD_CHANGED",
                "message_ar": "تم تغيير كلمة المرور بنجاح.",
                "table": f"{schema}.{table}",
            }

    except Exception as e:
        return {"ok": False, "code": "SERVER_ERROR", "message_ar": "حدث خطأ أثناء تغيير كلمة المرور.", "error": str(e)[:240]}
