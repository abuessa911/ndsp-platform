import json
import os
import re
import psycopg2
import psycopg2.extras
from starlette.responses import JSONResponse


def _db_url():
    return (
        os.getenv("AUTH_DATABASE_URL")
        or os.getenv("DATABASE_URL")
        or os.getenv("POSTGRES_URL")
        or ""
    )


def _email(v):
    return str(v or "").strip().lower()


def _phone(v):
    return re.sub(r"[\s\-\(\)]", "", str(v or "").strip())


def _table_exists(cur, table):
    cur.execute("select to_regclass(%s) as regclass", [table])
    row = cur.fetchone()
    if not row:
        return False
    if isinstance(row, dict):
        return bool(row.get("regclass"))
    return bool(row[0])


def _col_exists(cur, table, col):
    cur.execute("""
        select 1 as found
        from information_schema.columns
        where table_schema='public'
          and table_name=%s
          and column_name=%s
        limit 1
    """, [table, col])
    return cur.fetchone() is not None


def _duplicate_check(email, phone):
    url = _db_url()
    if not url:
        return None

    email = _email(email)
    phone = _phone(phone)

    with psycopg2.connect(url) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:

            if _table_exists(cur, "users"):
                has_phone = _col_exists(cur, "users", "phone")
                if has_phone:
                    cur.execute("""
                        select id::text as id, email, phone, status
                        from users
                        where lower(email)=lower(%s)
                           or regexp_replace(coalesce(phone,''), '[\\s\\-\\(\\)]', '', 'g')=%s
                        limit 1
                    """, [email, phone])
                else:
                    cur.execute("""
                        select id::text as id, email, null::text as phone, status
                        from users
                        where lower(email)=lower(%s)
                        limit 1
                    """, [email])

                row = cur.fetchone()
                if row:
                    if _email(row.get("email")) == email:
                        return ("DUPLICATE_EMAIL", "البريد الإلكتروني مستخدم سابقًا", "users", row.get("id"))
                    return ("DUPLICATE_PHONE", "رقم الجوال مستخدم سابقًا", "users", row.get("id"))

            for table in ("trial_activation_requests", "ndsp_trial_activation_requests"):
                if not _table_exists(cur, table):
                    continue

                cur.execute(f"""
                    select id::text as id, email, status, raw_payload
                    from {table}
                    where lower(email)=lower(%s)
                       or raw_payload::text ILIKE %s
                    limit 1
                """, [email, "%" + phone + "%"])

                row = cur.fetchone()
                if row:
                    raw = row.get("raw_payload") or {}
                    if isinstance(raw, str):
                        try:
                            raw = json.loads(raw)
                        except Exception:
                            raw = {}
                    raw_phone = _phone(raw.get("phone") if isinstance(raw, dict) else "")

                    if _email(row.get("email")) == email:
                        return ("PENDING_ACTIVATION_EXISTS", "يوجد طلب تفعيل سابق لهذا البريد.", table, row.get("id"))
                    if raw_phone == phone or phone in str(row.get("raw_payload") or ""):
                        return ("DUPLICATE_PHONE", "رقم الجوال مستخدم سابقًا", table, row.get("id"))

    return None


class NDSPTrialRegisterGuardMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path") or ""
        method = scope.get("method") or ""

        if method.upper() == "POST" and path.startswith("/api/trial/register/"):
            body = b""
            more_body = True

            while more_body:
                message = await receive()
                body += message.get("body", b"")
                more_body = message.get("more_body", False)

            try:
                data = json.loads(body.decode("utf-8") or "{}")
            except Exception:
                data = {}

            email = _email(data.get("email"))
            phone = _phone(data.get("phone"))

            if not email:
                response = JSONResponse({"ok": False, "code": "INVALID_EMAIL", "message": "البريد الإلكتروني مطلوب."}, status_code=200)
                await response(scope, receive, send)
                return

            if not phone:
                response = JSONResponse({"ok": False, "code": "INVALID_PHONE", "message": "رقم الجوال مطلوب."}, status_code=200)
                await response(scope, receive, send)
                return

            found = _duplicate_check(email, phone)
            if found:
                code, msg, source, row_id = found
                response = JSONResponse({
                    "ok": False,
                    "code": code,
                    "message": msg,
                    "duplicate_source": source,
                    "duplicate_id": row_id
                }, status_code=200)
                await response(scope, receive, send)
                return

            sent = False

            async def replay_receive():
                nonlocal sent
                if not sent:
                    sent = True
                    return {"type": "http.request", "body": body, "more_body": False}
                return {"type": "http.request", "body": b"", "more_body": False}

            await self.app(scope, replay_receive, send)
            return

        await self.app(scope, receive, send)
