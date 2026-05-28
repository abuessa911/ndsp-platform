from __future__ import annotations
from app.ndsp_db_env_loader import load_ndsp_db_env
load_ndsp_db_env(force=True)

import base64
import hashlib
import hmac
import os
import re
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, Field, validator
from sqlalchemy import create_engine, text

router = APIRouter(prefix="/api/v6/elite-trial", tags=["elite-trial-requests"])

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("NDSP_DATABASE_URL") or "sqlite:///./ndsp_elite_trial_requests.db"
ADMIN_KEY = os.getenv("NDSP_ADMIN_KEY") or os.getenv("ADMIN_KEY") or ""

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

ALLOWED_BUCKETS = {"ordinary", "professional", "featured"}
ALLOWED_STATUS = {"pending", "approved", "rejected", "reviewed"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def password_hash(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 220000)
    return "pbkdf2_sha256$220000$" + base64.b64encode(salt).decode() + "$" + base64.b64encode(digest).decode()


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, rounds, salt_b64, digest_b64 = stored.split("$", 3)
        if algo != "pbkdf2_sha256":
            return False
        salt = base64.b64decode(salt_b64.encode())
        expected = base64.b64decode(digest_b64.encode())
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, int(rounds))
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False


def require_admin(x_admin_key: Optional[str]) -> None:
    if not ADMIN_KEY:
        raise HTTPException(status_code=503, detail="admin authorization is not configured")
    if not x_admin_key or x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="admin authorization required")


class TrialRequestCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: str = Field(..., min_length=5, max_length=180)
    password: str = Field(..., min_length=8, max_length=128)
    bucket: str = "ordinary"
    contact_channel: str = Field(default="email", max_length=40)
    reason: str = Field(default="", max_length=1200)

    @validator("name", "email", "bucket", "contact_channel", "reason", pre=True, always=True)
    def clean_text(cls, value):
        return clean(value)

    @validator("email")
    def validate_email(cls, value):
        value = value.lower().strip()
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("invalid email")
        return value

    @validator("bucket")
    def validate_bucket(cls, value):
        value = value.lower().strip()
        if value not in ALLOWED_BUCKETS:
            return "ordinary"
        return value

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("password must be at least 8 characters")
        return value


class TrialRequestUpdate(BaseModel):
    status: str
    admin_note: Optional[str] = ""

    @validator("status")
    def validate_status(cls, value):
        value = clean(value).lower()
        if value not in ALLOWED_STATUS:
            raise ValueError("invalid status")
        return value

    @validator("admin_note", pre=True, always=True)
    def clean_note(cls, value):
        return clean(value)


class TrialLogin(BaseModel):
    email: str
    password: str

    @validator("email", pre=True, always=True)
    def clean_email(cls, value):
        return clean(value).lower()


def table_columns(conn) -> set[str]:
    backend_name = engine.url.get_backend_name()
    if backend_name.startswith("postgres"):
        rows = conn.execute(
            text(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'elite_trial_requests'
                """
            )
        ).fetchall()
        return {row._mapping["column_name"] for row in rows}

    rows = conn.execute(text("PRAGMA table_info(elite_trial_requests)")).fetchall()
    return {row._mapping["name"] for row in rows}


def add_column_if_missing(conn, columns: set[str], name: str, ddl_type: str) -> None:
    if name not in columns:
        conn.execute(text(f"ALTER TABLE elite_trial_requests ADD COLUMN {name} {ddl_type}"))


def init_table() -> None:
    backend_name = engine.url.get_backend_name()

    if backend_name.startswith("postgres"):
        ddl = """
        CREATE TABLE IF NOT EXISTS elite_trial_requests (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password_hash TEXT DEFAULT '',
            bucket TEXT NOT NULL DEFAULT 'ordinary',
            contact_channel TEXT NOT NULL DEFAULT 'email',
            reason TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            admin_note TEXT DEFAULT '',
            source_ip TEXT DEFAULT '',
            user_agent TEXT DEFAULT '',
            approved_at TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
    else:
        ddl = """
        CREATE TABLE IF NOT EXISTS elite_trial_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password_hash TEXT DEFAULT '',
            bucket TEXT NOT NULL DEFAULT 'ordinary',
            contact_channel TEXT NOT NULL DEFAULT 'email',
            reason TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'pending',
            admin_note TEXT DEFAULT '',
            source_ip TEXT DEFAULT '',
            user_agent TEXT DEFAULT '',
            approved_at TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """

    with engine.begin() as conn:
        conn.execute(text(ddl))
        columns = table_columns(conn)
        add_column_if_missing(conn, columns, "password_hash", "TEXT DEFAULT ''")
        add_column_if_missing(conn, columns, "approved_at", "TEXT DEFAULT ''")
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_elite_trial_email ON elite_trial_requests(email);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_elite_trial_status ON elite_trial_requests(status);"))


def row_to_dict(row) -> dict:
    item = dict(row._mapping)
    item.pop("password_hash", None)
    return item


@router.get("/health")
def elite_trial_requests_health() -> dict:
    init_table()
    return {
        "ok": True,
        "service": "elite-trial-requests",
        "database": "ready",
        "password_flow": "enabled",
        "admin_auth_configured": bool(ADMIN_KEY),
    }


@router.post("/requests")
def create_trial_request(payload: TrialRequestCreate, request: Request) -> dict:
    init_table()

    email = payload.email.lower().strip()
    timestamp = now_iso()
    source_ip = request.client.host if request.client else ""
    user_agent = request.headers.get("user-agent", "")[:300]
    hashed = password_hash(payload.password)

    with engine.begin() as conn:
        existing = conn.execute(
            text("SELECT id, status FROM elite_trial_requests WHERE lower(email)=lower(:email) ORDER BY id DESC LIMIT 1"),
            {"email": email},
        ).fetchone()

        if existing:
            return {
                "ok": True,
                "duplicate": True,
                "message": "request already exists",
                "request_id": int(existing._mapping["id"]),
                "status": existing._mapping["status"],
            }

        params = {
            "name": payload.name,
            "email": email,
            "password_hash": hashed,
            "bucket": payload.bucket,
            "contact_channel": payload.contact_channel,
            "reason": payload.reason,
            "source_ip": source_ip,
            "user_agent": user_agent,
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        if engine.url.get_backend_name().startswith("postgres"):
            row = conn.execute(
                text(
                    """
                    INSERT INTO elite_trial_requests
                    (name, email, password_hash, bucket, contact_channel, reason, status, admin_note, source_ip, user_agent, approved_at, created_at, updated_at)
                    VALUES
                    (:name, :email, :password_hash, :bucket, :contact_channel, :reason, 'pending', '', :source_ip, :user_agent, '', :created_at, :updated_at)
                    RETURNING id, status
                    """
                ),
                params,
            ).fetchone()
        else:
            conn.execute(
                text(
                    """
                    INSERT INTO elite_trial_requests
                    (name, email, password_hash, bucket, contact_channel, reason, status, admin_note, source_ip, user_agent, approved_at, created_at, updated_at)
                    VALUES
                    (:name, :email, :password_hash, :bucket, :contact_channel, :reason, 'pending', '', :source_ip, :user_agent, '', :created_at, :updated_at)
                    """
                ),
                params,
            )
            row = conn.execute(
                text("SELECT id, status FROM elite_trial_requests WHERE lower(email)=lower(:email) ORDER BY id DESC LIMIT 1"),
                {"email": email},
            ).fetchone()

    return {
        "ok": True,
        "duplicate": False,
        "message": "trial request received",
        "request_id": int(row._mapping["id"]),
        "status": row._mapping["status"],
    }


@router.get("/requests")
def list_trial_requests(
    status: Optional[str] = None,
    x_admin_key: Optional[str] = Header(default=None, alias="X-Admin-Key"),
) -> dict:
    require_admin(x_admin_key)
    init_table()

    params = {}
    where = ""

    if status:
        status = status.lower().strip()
        if status not in ALLOWED_STATUS:
            raise HTTPException(status_code=422, detail="invalid status")
        where = "WHERE status=:status"
        params["status"] = status

    with engine.begin() as conn:
        rows = conn.execute(
            text(
                f"""
                SELECT id, name, email, bucket, contact_channel, reason, status, admin_note, source_ip, approved_at, created_at, updated_at
                FROM elite_trial_requests
                {where}
                ORDER BY id DESC
                LIMIT 500
                """
            ),
            params,
        ).fetchall()

    return {
        "ok": True,
        "items": [row_to_dict(row) for row in rows],
    }


@router.patch("/requests/{request_id}")
def update_trial_request(
    request_id: int,
    payload: TrialRequestUpdate,
    x_admin_key: Optional[str] = Header(default=None, alias="X-Admin-Key"),
) -> dict:
    require_admin(x_admin_key)
    init_table()

    timestamp = now_iso()
    approved_at = timestamp if payload.status == "approved" else ""

    with engine.begin() as conn:
        existing = conn.execute(
            text("SELECT id FROM elite_trial_requests WHERE id=:id"),
            {"id": request_id},
        ).fetchone()

        if not existing:
            raise HTTPException(status_code=404, detail="request not found")

        conn.execute(
            text(
                """
                UPDATE elite_trial_requests
                SET status=:status,
                    admin_note=:admin_note,
                    approved_at=CASE WHEN :status = 'approved' THEN :approved_at ELSE approved_at END,
                    updated_at=:updated_at
                WHERE id=:id
                """
            ),
            {
                "id": request_id,
                "status": payload.status,
                "admin_note": payload.admin_note or "",
                "approved_at": approved_at,
                "updated_at": timestamp,
            },
        )

        row = conn.execute(
            text(
                """
                SELECT id, name, email, bucket, contact_channel, reason, status, admin_note, source_ip, approved_at, created_at, updated_at
                FROM elite_trial_requests
                WHERE id=:id
                """
            ),
            {"id": request_id},
        ).fetchone()

    return {
        "ok": True,
        "item": row_to_dict(row),
    }


@router.post("/login")
def elite_trial_login(payload: TrialLogin) -> dict:
    init_table()

    with engine.begin() as conn:
        row = conn.execute(
            text(
                """
                SELECT id, name, email, password_hash, status, bucket, approved_at
                FROM elite_trial_requests
                WHERE lower(email)=lower(:email)
                ORDER BY id DESC
                LIMIT 1
                """
            ),
            {"email": payload.email},
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="trial account not found")

    item = dict(row._mapping)
    if not verify_password(payload.password, item.get("password_hash") or ""):
        raise HTTPException(status_code=403, detail="invalid credentials")

    if item.get("status") != "approved":
        raise HTTPException(status_code=403, detail="trial account is not approved yet")

    return {
        "ok": True,
        "active": True,
        "trial_access": "approved",
        "request_id": int(item["id"]),
        "name": item["name"],
        "email": item["email"],
        "bucket": item["bucket"],
        "approved_at": item.get("approved_at") or "",
    }
