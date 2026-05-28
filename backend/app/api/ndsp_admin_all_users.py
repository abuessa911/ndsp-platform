from fastapi import APIRouter, Header, HTTPException, Query
from typing import Optional, Dict, Any, List
import os
import psycopg2
import psycopg2.extras

router = APIRouter()

def admin_key() -> str:
    for k in ("ADMIN_KEY", "NDSP_ADMIN_KEY", "ADMIN_API_KEY"):
        v = (os.getenv(k) or "").strip()
        if v:
            return v
    return ""

def require_admin(x_admin_key: Optional[str] = Header(default=None, alias="x-admin-key")):
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

def rows(sql: str, params=None) -> List[Dict[str, Any]]:
    url = db_url()
    if not url:
        return []
    with psycopg2.connect(url) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params or [])
            return [dict(r) for r in cur.fetchall()]

def table_exists(name: str) -> bool:
    try:
        r = rows("select to_regclass(%s) as t", [name])
        return bool(r and r[0].get("t"))
    except Exception:
        return False

@router.get("/api/admin/users/all")
def admin_users_all(limit: int = Query(default=100, ge=1, le=500), _: None = None, x_admin_key: Optional[str] = Header(default=None, alias="x-admin-key")):
    require_admin(x_admin_key)

    output = {
        "ok": True,
        "source": "ndsp_admin_all_users",
        "users": [],
        "trial_activation_requests": [],
        "plan_upgrade_requests": [],
        "counts": {}
    }

    if table_exists("users"):
        output["users"] = rows("""
            select id, email, name, role, plan, status, created_at
            from users
            order by id desc
            limit %s
        """, [limit])

    if table_exists("ndsp_trial_activation_requests"):
        output["trial_activation_requests"] = rows("""
            select id, category, email, name, status, source_path, created_at, updated_at
            from ndsp_trial_activation_requests
            order by id desc
            limit %s
        """, [limit])
    elif table_exists("trial_activation_requests"):
        output["trial_activation_requests"] = rows("""
            select id, category, email, name, status, source_path, created_at, updated_at
            from trial_activation_requests
            order by id desc
            limit %s
        """, [limit])

    if table_exists("plan_upgrade_requests"):
        output["plan_upgrade_requests"] = rows("""
            select *
            from plan_upgrade_requests
            order by id desc
            limit %s
        """, [limit])

    output["counts"] = {
        "users": len(output["users"]),
        "trial_activation_requests": len(output["trial_activation_requests"]),
        "plan_upgrade_requests": len(output["plan_upgrade_requests"]),
        "total_visible": len(output["users"]) + len(output["trial_activation_requests"]) + len(output["plan_upgrade_requests"])
    }

    return output
