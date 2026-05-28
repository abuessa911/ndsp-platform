from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import psycopg2
import psycopg2.extras

router = APIRouter()

class CheckReq(BaseModel):
    email: str

def db_url() -> str:
    return os.getenv("AUTH_DATABASE_URL") or os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or ""

def admin_key() -> str:
    for k in ("ADMIN_KEY", "NDSP_ADMIN_KEY", "ADMIN_API_KEY"):
        v = (os.getenv(k) or "").strip()
        if v:
            return v
    return ""

def require_admin(x_admin_key: Optional[str]):
    if not admin_key() or not x_admin_key or x_admin_key.strip() != admin_key():
        raise HTTPException(status_code=401, detail="INVALID_ADMIN_KEY")

def table_exists(cur, name: str) -> bool:
    cur.execute("select to_regclass(%s)", [name])
    return bool(cur.fetchone()[0])

@router.post("/api/admin/trial-activations/dedupe-pending")
def dedupe_pending(x_admin_key: Optional[str] = Header(default=None, alias="x-admin-key")):
    require_admin(x_admin_key)

    url = db_url()
    if not url:
        raise HTTPException(status_code=500, detail="DATABASE_URL_MISSING")

    deleted_total = 0
    kept = []

    with psycopg2.connect(url) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            for table in ("trial_activation_requests", "ndsp_trial_activation_requests"):
                if not table_exists(cur, table):
                    continue

                cur.execute(f"""
                    SELECT lower(email) AS email, max(id) AS keep_id, count(*) AS cnt
                    FROM {table}
                    WHERE status = 'pending_admin_review'
                    GROUP BY lower(email)
                    HAVING count(*) > 1
                """)
                groups = cur.fetchall()

                for g in groups:
                    cur.execute(
                        f"""
                        DELETE FROM {table}
                        WHERE status = 'pending_admin_review'
                          AND lower(email) = %s
                          AND id <> %s
                        """,
                        [g["email"], g["keep_id"]]
                    )
                    deleted_total += cur.rowcount
                    kept.append({"email": g["email"], "keep_id": g["keep_id"], "original_count": g["cnt"]})

            conn.commit()

    return {"ok": True, "deleted_duplicates": deleted_total, "kept": kept}

@router.post("/api/admin/trial-activations/check-email")
def check_email(req: CheckReq, x_admin_key: Optional[str] = Header(default=None, alias="x-admin-key")):
    require_admin(x_admin_key)

    email = req.email.strip().lower()
    url = db_url()
    if not url:
        raise HTTPException(status_code=500, detail="DATABASE_URL_MISSING")

    with psycopg2.connect(url) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            for table in ("trial_activation_requests", "ndsp_trial_activation_requests"):
                if not table_exists(cur, table):
                    continue

                cur.execute(
                    f"""
                    SELECT id,email,name,status,category,created_at
                    FROM {table}
                    WHERE lower(email) = %s
                    ORDER BY id DESC
                    LIMIT 10
                    """,
                    [email]
                )
                rows = cur.fetchall()
                if rows:
                    return {"ok": True, "table": table, "items": [dict(r) for r in rows], "count": len(rows)}

    return {"ok": True, "items": [], "count": 0}
