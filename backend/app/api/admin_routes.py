import os
from typing import Optional, Any, Dict, List

import psycopg2
import psycopg2.extras
from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel

router = APIRouter(prefix="/api/admin", tags=["admin"])

def _env_first(*names: str, default: Optional[str] = None) -> Optional[str]:
    for name in names:
        val = os.environ.get(name)
        if val:
            return val
    return default

def _admin_key() -> Optional[str]:
    return _env_first("NDSP_ADMIN_KEY", "ADMIN_KEY", "ADMIN_API_KEY", "X_ADMIN_KEY")

def _require_admin(
    x_admin_key: Optional[str] = Header(default=None),
    authorization: Optional[str] = Header(default=None),
) -> None:
    expected = _admin_key()
    if not expected:
        raise HTTPException(status_code=500, detail="ADMIN_KEY_NOT_CONFIGURED")

    provided = x_admin_key
    if not provided and authorization:
        if authorization.lower().startswith("bearer "):
            provided = authorization.split(" ", 1)[1].strip()
        else:
            provided = authorization.strip()

    if provided != expected:
        raise HTTPException(status_code=401, detail="INVALID_ADMIN_KEY")

def _conn():
    db_url = _env_first("DATABASE_URL", "POSTGRES_URL")
    if db_url:
        return psycopg2.connect(db_url, cursor_factory=psycopg2.extras.RealDictCursor)

    return psycopg2.connect(
        host=_env_first("PGHOST", "DB_HOST", default="127.0.0.1"),
        port=int(_env_first("PGPORT", "DB_PORT", default="5432") or "5432"),
        dbname=_env_first("PGDATABASE", "DB_NAME", "POSTGRES_DB", default="ndsp_auth"),
        user=_env_first("PGUSER", "DB_USER", "POSTGRES_USER", default="ndsp_auth"),
        password=_env_first("PGPASSWORD", "DB_PASSWORD", "POSTGRES_PASSWORD", default=""),
        cursor_factory=psycopg2.extras.RealDictCursor,
    )

def _table_exists(cur, table: str) -> bool:
    cur.execute("select to_regclass(%s) as reg", (table,))
    row = cur.fetchone() or {}
    return bool(row.get("reg"))

def _safe_count(cur, table: str, where: str = "", params: tuple = ()) -> int:
    if not _table_exists(cur, table):
        return 0
    cur.execute(f"select count(*) as c from {table} {where}", params)
    return int((cur.fetchone() or {}).get("c") or 0)

def _detect_activation_table(cur) -> Optional[str]:
    for table in (
        "trial_activation_requests",
        "ndsp_trial_activation_requests",
        "plan_upgrade_requests",
    ):
        try:
            cur.execute("select to_regclass(%s) as regclass", [table])
            row = cur.fetchone()
            exists = False
            if row:
                if isinstance(row, dict):
                    exists = bool(row.get("regclass"))
                else:
                    exists = bool(row[0])
            if exists:
                return table
        except Exception:
            continue
    return None

def _fetch_table_rows(cur, table: str, limit: int = 200) -> List[Dict[str, Any]]:
    if not table or not _table_exists(cur, table):
        return []

    cur.execute("""
        select column_name
        from information_schema.columns
        where table_schema='public' and table_name=%s
        order by ordinal_position
    """, (table,))
    cols = [r["column_name"] for r in cur.fetchall()]

    order_col = None
    for c in ["created_at", "updated_at", "id"]:
        if c in cols:
            order_col = c
            break

    sql = f"select * from {table}"
    if order_col:
        sql += f" order by {order_col} desc"
    sql += " limit %s"
    cur.execute(sql, (limit,))
    return [dict(r) for r in cur.fetchall()]

class InviteCreateRequest(BaseModel):
    count: int = 1
    category: str = "premium_invite_only"
    note: Optional[str] = None

@router.get("/seats")
def admin_seats(
    x_admin_key: Optional[str] = Header(default=None),
    authorization: Optional[str] = Header(default=None),
):
    _require_admin(x_admin_key, authorization)
    with _conn() as conn:
        with conn.cursor() as cur:
            normal = _safe_count(cur, "users", "where plan = %s", ("trial",))
            activation_table = _detect_activation_table(cur)
            pending = approved = rejected = 0
            if activation_table:
                pending = _safe_count(cur, activation_table, "where status = %s", ("pending_admin_review",))
                approved = _safe_count(cur, activation_table, "where status = %s", ("approved",))
                rejected = _safe_count(cur, activation_table, "where status = %s", ("rejected",))

            return {
                "ok": True,
                "source": "fastapi_admin",
                "database": {"connected": True, "name": conn.info.dbname, "user": conn.info.user, "password_exposed": False},
                "quotas": {"specialist_academic": 10, "normal_beginner": 25, "premium_invite_only": 15, "total": 50},
                "used": {"normal_beginner": normal, "activation_pending": pending, "activation_approved": approved, "activation_rejected": rejected},
                "activation_table": activation_table,
            }

@router.get("/users/trial")
def admin_users_trial(
    x_admin_key: Optional[str] = Header(default=None),
    authorization: Optional[str] = Header(default=None),
):
    _require_admin(x_admin_key, authorization)
    with _conn() as conn:
        with conn.cursor() as cur:
            table = _detect_activation_table(cur)
            rows = _fetch_table_rows(cur, table, 300) if table else []
            return {
                "ok": True,
                "source": "fastapi_admin",
                "table": table,
                "count": len(rows),
                "items": rows,
                "requests": rows,
            }

@router.get("/assets")
def admin_assets(
    x_admin_key: Optional[str] = Header(default=None),
    authorization: Optional[str] = Header(default=None),
):
    _require_admin(x_admin_key, authorization)
    with _conn() as conn:
        with conn.cursor() as cur:
            tables = {}
            for t in ["users", "trial_activation_requests", "activation_requests", "trial_requests", "trial_registrations", "trial_invites", "premium_invites"]:
                tables[t] = _table_exists(cur, t)
            return {
                "ok": True,
                "source": "fastapi_admin",
                "database": {"connected": True, "name": conn.info.dbname, "user": conn.info.user, "password_exposed": False},
                "tables": tables,
                "api_base": "/api",
                "legacy_api_v7": "retired_404",
            }

@router.post("/invitations/create")
def admin_create_invitation(
    payload: InviteCreateRequest,
    x_admin_key: Optional[str] = Header(default=None),
    authorization: Optional[str] = Header(default=None),
):
    _require_admin(x_admin_key, authorization)
    # Safe placeholder until invitation schema is finalized
    return {
        "ok": True,
        "source": "fastapi_admin",
        "created": 0,
        "message": "Invitation creation endpoint is active. Schema write is intentionally not performed unless invite table contract is finalized.",
        "requested": payload.dict(),
    }
