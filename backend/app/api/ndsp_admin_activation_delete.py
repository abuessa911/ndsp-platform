from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import psycopg2

router = APIRouter()

class DeleteReq(BaseModel):
    id: int

def admin_key() -> str:
    for k in ("ADMIN_KEY", "NDSP_ADMIN_KEY", "ADMIN_API_KEY"):
        v = (os.getenv(k) or "").strip()
        if v:
            return v
    return ""

def require_admin(x_admin_key: Optional[str]):
    expected = admin_key()
    if not expected or not x_admin_key or x_admin_key.strip() != expected:
        raise HTTPException(status_code=401, detail="INVALID_ADMIN_KEY")

def db_url() -> str:
    return (
        os.getenv("AUTH_DATABASE_URL")
        or os.getenv("DATABASE_URL")
        or os.getenv("POSTGRES_URL")
        or ""
    )

@router.post("/api/admin/trial-activations/delete")
def delete_activation(
    req: DeleteReq,
    x_admin_key: Optional[str] = Header(default=None, alias="x-admin-key"),
):
    require_admin(x_admin_key)

    url = db_url()
    if not url:
        raise HTTPException(status_code=500, detail="DATABASE_URL_MISSING")

    tables = ("trial_activation_requests", "ndsp_trial_activation_requests")

    with psycopg2.connect(url) as conn:
        with conn.cursor() as cur:
            for table in tables:
                cur.execute("select to_regclass(%s)", [table])
                exists = cur.fetchone()[0]
                if exists:
                    cur.execute(f"delete from {table} where id = %s", [req.id])
                    rows = cur.rowcount
                    conn.commit()
                    return {
                        "ok": True,
                        "deleted_id": req.id,
                        "table": table,
                        "rows": rows,
                    }

    return {"ok": False, "error": "TABLE_NOT_FOUND"}
