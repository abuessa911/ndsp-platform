from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import json
import secrets
import hashlib
import psycopg2
import psycopg2.extras

router = APIRouter()

class ApproveReq(BaseModel):
    id: int
    admin_note: Optional[str] = "Approved from admin panel"

def admin_key() -> str:
    for k in ("ADMIN_KEY", "NDSP_ADMIN_KEY", "ADMIN_API_KEY"):
        v = (os.getenv(k) or "").strip()
        if v:
            return v
    return ""

def require_admin(x_admin_key: Optional[str]) -> None:
    expected = admin_key()
    if not expected or not x_admin_key or x_admin_key.strip() != expected:
        raise HTTPException(status_code=401, detail="INVALID_ADMIN_KEY")

def db_url() -> str:
    return os.getenv("AUTH_DATABASE_URL") or os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or ""

def table_exists(conn, table: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("select to_regclass(%s)", [table])
        row = cur.fetchone()
        return bool(row and row[0])

def column_exists(conn, table: str, column: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("""
            select 1
            from information_schema.columns
            where table_schema='public'
              and table_name=%s
              and column_name=%s
            limit 1
        """, [table, column])
        return cur.fetchone() is not None

def add_column(conn, table: str, definition: str) -> None:
    with conn.cursor() as cur:
        cur.execute(f"alter table {table} add column if not exists {definition}")

def ensure_optional_user_columns(conn) -> None:
    for definition in (
        "category text",
        "phone text",
        "trial_ends_at timestamptz",
        "plan_id integer",
    ):
        add_column(conn, "users", definition)

def placeholder_hash(email: str) -> str:
    raw = "ndsp-approved-placeholder:" + email + ":" + secrets.token_urlsafe(16)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def get_activation(conn, activation_id: int):
    activation_table = None
    for t in ("trial_activation_requests", "ndsp_trial_activation_requests"):
        if table_exists(conn, t):
            activation_table = t
            break

    if not activation_table:
        raise HTTPException(status_code=500, detail="ACTIVATION_TABLE_NOT_FOUND")

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f"select * from {activation_table} where id=%s", [activation_id])
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="ACTIVATION_REQUEST_NOT_FOUND")

    return activation_table, dict(row)

@router.post("/api/admin/trial-activations/approve-user")
def approve_user(req: ApproveReq, x_admin_key: Optional[str] = Header(default=None, alias="x-admin-key")):
    require_admin(x_admin_key)

    url = db_url()
    if not url:
        raise HTTPException(status_code=500, detail="DATABASE_URL_MISSING")

    with psycopg2.connect(url) as conn:
        activation_table, activation = get_activation(conn, req.id)

        raw = activation.get("raw_payload") or {}
        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except Exception:
                raw = {}

        email = (activation.get("email") or raw.get("email") or "").strip().lower()
        name = activation.get("name") or raw.get("name") or email
        category = activation.get("category") or raw.get("category") or "specialist_academic"
        phone = raw.get("phone") or ""

        if not email:
            raise HTTPException(status_code=400, detail="EMAIL_MISSING")

        if not table_exists(conn, "users"):
            raise HTTPException(status_code=500, detail="USERS_TABLE_NOT_FOUND")

        ensure_optional_user_columns(conn)

        with conn.cursor() as cur:
            cur.execute(f"""
                update {activation_table}
                set status='approved',
                    approved_at=now(),
                    approved_by='admin-panel',
                    admin_note=%s,
                    updated_at=now()
                where id=%s
            """, [req.admin_note, req.id])

        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("select id from users where lower(email)=lower(%s) limit 1", [email])
            existing = cur.fetchone()

            if existing:
                cur.execute("""
                    update users
                    set
                        name=%s,
                        plan='Elite',
                        role='user',
                        status='active',
                        trial_day=1,
                        trial_started_at=coalesce(trial_started_at, now()),
                        trial_ends_at=now() + interval '16 days',
                        category=%s,
                        phone=coalesce(nullif(%s,''), phone)
                    where id=%s
                    returning id,email,name,status,plan,role,trial_day,trial_started_at,trial_ends_at,category,phone
                """, [name, category, phone, existing["id"]])
            else:
                cur.execute("""
                    insert into users
                    (
                        name,
                        email,
                        password_hash,
                        plan,
                        role,
                        trial_day,
                        trial_started_at,
                        created_at,
                        status,
                        trial_ends_at,
                        category,
                        phone
                    )
                    values
                    (
                        %s,
                        %s,
                        %s,
                        'Elite',
                        'user',
                        1,
                        now(),
                        now(),
                        'active',
                        now() + interval '16 days',
                        %s,
                        %s
                    )
                    returning id,email,name,status,plan,role,trial_day,trial_started_at,trial_ends_at,category,phone
                """, [name, email, placeholder_hash(email), category, phone])

            user = dict(cur.fetchone())

        conn.commit()

    return {
        "ok": True,
        "activation_id": req.id,
        "activation_status": "approved",
        "user": user,
        "trial_days": 16
    }
