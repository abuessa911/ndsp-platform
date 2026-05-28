from fastapi import Request
from fastapi.responses import JSONResponse
import os
import json
import psycopg2
import psycopg2.extras

def _db_url() -> str:
    return (
        os.getenv("AUTH_DATABASE_URL")
        or os.getenv("DATABASE_URL")
        or os.getenv("POSTGRES_URL")
        or ""
    )

def _normalize_email(v: str) -> str:
    return (v or "").strip().lower()

def _normalize_phone(v: str) -> str:
    return (v or "").strip().replace(" ", "").replace("-", "")

def _table_exists(cur, table: str) -> bool:
    cur.execute("select to_regclass(%s) as regclass", [table])
    row = cur.fetchone()
    if not row:
        return False
    if isinstance(row, dict):
        return bool(row.get("regclass"))
    return bool(row[0])

def _col_exists(cur, table: str, col: str) -> bool:
    cur.execute("""
        select 1
        from information_schema.columns
        where table_schema='public'
          and table_name=%s
          and column_name=%s
        limit 1
    """, [table, col])
    return cur.fetchone() is not None

def _json_phone_expr(table: str) -> str:
    return "raw_payload::text ILIKE %s"

def _existing_email_or_phone(email: str, phone: str):
    url = _db_url()
    if not url:
        return None

    email = _normalize_email(email)
    phone = _normalize_phone(phone)

    with psycopg2.connect(url) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            # 1) users table
            if _table_exists(cur, "users"):
                has_phone = _col_exists(cur, "users", "phone")
                if has_phone:
                    cur.execute("""
                        select 'users' as source, id::text as id, email, phone, status
                        from users
                        where lower(email)=lower(%s)
                           or regexp_replace(coalesce(phone,''), '[\\s-]', '', 'g') = %s
                        limit 1
                    """, [email, phone])
                else:
                    cur.execute("""
                        select 'users' as source, id::text as id, email, null::text as phone, status
                        from users
                        where lower(email)=lower(%s)
                        limit 1
                    """, [email])
                row = cur.fetchone()
                if row:
                    if _normalize_email(row.get("email")) == email:
                        return {"code": "DUPLICATE_EMAIL", "message": "البريد الإلكتروني مستخدم سابقًا", "row": dict(row)}
                    return {"code": "DUPLICATE_PHONE", "message": "رقم الجوال مستخدم سابقًا", "row": dict(row)}

            # 2) activation tables
            for table in ("trial_activation_requests", "ndsp_trial_activation_requests"):
                if not _table_exists(cur, table):
                    continue

                cur.execute(f"""
                    select %s as source, id::text as id, email, status, raw_payload
                    from {table}
                    where lower(email)=lower(%s)
                       or raw_payload::text ILIKE %s
                    limit 1
                """, [table, email, "%" + phone + "%"])
                row = cur.fetchone()
                if row:
                    raw = row.get("raw_payload") or {}
                    if isinstance(raw, str):
                        try:
                            raw = json.loads(raw)
                        except Exception:
                            raw = {}
                    row_phone = _normalize_phone(raw.get("phone") if isinstance(raw, dict) else "")
                    if _normalize_email(row.get("email")) == email:
                        return {"code": "PENDING_ACTIVATION_EXISTS", "message": "يوجد طلب تفعيل سابق لهذا البريد.", "row": dict(row)}
                    if row_phone == phone or phone in str(row.get("raw_payload") or ""):
                        return {"code": "DUPLICATE_PHONE", "message": "رقم الجوال مستخدم سابقًا", "row": dict(row)}

            # 3) plan upgrade requests
            for table in ("plan_upgrade_requests",):
                if not _table_exists(cur, table):
                    continue

                has_email = _col_exists(cur, table, "email")
                has_raw = _col_exists(cur, table, "raw_payload")

                conditions = []
                params = [table]

                if has_email:
                    conditions.append("lower(email)=lower(%s)")
                    params.append(email)

                if has_raw:
                    conditions.append("raw_payload::text ILIKE %s")
                    params.append("%" + phone + "%")

                if conditions:
                    cur.execute(
                        f"select %s as source, id::text as id, email from {table} where " + " or ".join(conditions) + " limit 1",
                        params
                    )
                    row = cur.fetchone()
                    if row:
                        if _normalize_email(row.get("email")) == email:
                            return {"code": "DUPLICATE_EMAIL", "message": "البريد الإلكتروني مستخدم سابقًا", "row": dict(row)}
                        return {"code": "DUPLICATE_PHONE", "message": "رقم الجوال مستخدم سابقًا", "row": dict(row)}

    return None

async def strict_email_phone_trial_guard(request: Request):
    try:
        body = await request.json()
    except Exception:
        return None

    email = _normalize_email(str(body.get("email") or ""))
    phone = _normalize_phone(str(body.get("phone") or ""))

    if not email:
        return JSONResponse(status_code=200, content={
            "ok": False,
            "code": "INVALID_EMAIL",
            "message": "البريد الإلكتروني مطلوب."
        })

    if not phone:
        return JSONResponse(status_code=200, content={
            "ok": False,
            "code": "INVALID_PHONE",
            "message": "رقم الجوال مطلوب."
        })

    found = _existing_email_or_phone(email, phone)
    if found:
        return JSONResponse(status_code=200, content={
            "ok": False,
            "code": found["code"],
            "message": found["message"],
            "duplicate_source": found["row"].get("source"),
            "duplicate_id": found["row"].get("id"),
        })

    return None
