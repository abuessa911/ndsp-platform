from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import os
import json
import psycopg2
import psycopg2.extras

router = APIRouter()

def _db_url():
    return os.getenv("AUTH_DATABASE_URL") or os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or ""

def _find_pending(email: str):
    email = (email or "").strip().lower()
    if not email:
        return None

    url = _db_url()
    if not url:
        return None

    with psycopg2.connect(url) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            for table in ("trial_activation_requests", "ndsp_trial_activation_requests"):
                cur.execute("select to_regclass(%s) as t", [table])
                if not cur.fetchone()["t"]:
                    continue

                cur.execute(
                    f"""
                    select id, email, status, category, created_at
                    from {table}
                    where lower(email) = %s
                      and status in ('pending_admin_review','pending','PENDING_ADMIN_REVIEW')
                    order by id desc
                    limit 1
                    """,
                    [email],
                )
                row = cur.fetchone()
                if row:
                    return dict(row)

    return None

async def duplicate_activation_guard(request: Request):
    try:
        body = await request.json()
    except Exception:
        return None

    email = str(body.get("email") or "").strip().lower()
    pending = _find_pending(email)

    if pending:
        return JSONResponse(
            status_code=200,
            content={
                "ok": False,
                "code": "PENDING_ACTIVATION_EXISTS",
                "message": "يوجد طلب تفعيل سابق قيد المراجعة لهذا البريد.",
                "existing_request": {
                    "id": pending.get("id"),
                    "email": pending.get("email"),
                    "status": pending.get("status"),
                    "category": pending.get("category"),
                    "created_at": str(pending.get("created_at")),
                },
            },
        )

    return None
