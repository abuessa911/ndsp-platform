from __future__ import annotations
from app.ndsp_db_env_loader import load_ndsp_db_env
load_ndsp_db_env(force=True)

import hashlib
import hmac
import json
import os
import secrets
import smtplib
import ssl
import uuid
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from typing import Any, Dict, Optional

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from app.core.elite_trial_capacity import enforce_elite_trial_capacity


def _database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError("DATABASE_URL is missing")
    return url


def _app_url() -> str:
    return os.getenv("NDSP_PUBLIC_APP_URL", "https://app.ndsp.app").strip().rstrip("/")


def _now():
    return datetime.now(timezone.utc)


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _normalize_email(email: str) -> str:
    return str(email or "").strip().lower()


def _normalize_phone(phone: str) -> str:
    raw = str(phone or "").strip()
    keep = []
    for ch in raw:
        if ch.isdigit() or ch == "+":
            keep.append(ch)
    phone = "".join(keep)
    if phone.startswith("00"):
        phone = "+" + phone[2:]
    return phone


def _client_ip(request) -> str:
    xff = request.headers.get("x-forwarded-for", "")
    if xff:
        return xff.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


def _user_agent(request) -> str:
    return request.headers.get("user-agent", "")[:500]


def get_conn():
    return psycopg.connect(_database_url(), row_factory=dict_row)


def init_auth_schema() -> Dict[str, Any]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS ndsp_auth_users (
                    id UUID PRIMARY KEY,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT UNIQUE,
                    name TEXT,
                    plan TEXT NOT NULL DEFAULT 'Elite',
                    category TEXT NOT NULL DEFAULT 'ordinary',
                    status TEXT NOT NULL DEFAULT 'ACTIVE',
                    trial_started_at TIMESTAMPTZ,
                    trial_ends_at TIMESTAMPTZ,
                    activated_at TIMESTAMPTZ,
                    last_login_at TIMESTAMPTZ,
                    ip_hash TEXT,
                    fingerprint_hash TEXT,
                    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS ndsp_auth_activation_tokens (
                    id UUID PRIMARY KEY,
                    user_id UUID NOT NULL REFERENCES ndsp_auth_users(id) ON DELETE CASCADE,
                    token_hash TEXT NOT NULL UNIQUE,
                    purpose TEXT NOT NULL DEFAULT 'email_activation',
                    used_at TIMESTAMPTZ,
                    expires_at TIMESTAMPTZ NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS ndsp_auth_sessions (
                    id UUID PRIMARY KEY,
                    user_id UUID NOT NULL REFERENCES ndsp_auth_users(id) ON DELETE CASCADE,
                    session_hash TEXT NOT NULL UNIQUE,
                    expires_at TIMESTAMPTZ NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """
            )

            cur.execute("CREATE INDEX IF NOT EXISTS ix_ndsp_auth_users_status ON ndsp_auth_users(status);")
            cur.execute("CREATE INDEX IF NOT EXISTS ix_ndsp_auth_users_category ON ndsp_auth_users(category);")
            cur.execute("CREATE INDEX IF NOT EXISTS ix_ndsp_auth_tokens_user ON ndsp_auth_activation_tokens(user_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS ix_ndsp_auth_sessions_user ON ndsp_auth_sessions(user_id);")

        conn.commit()

    return {"ok": True, "schema": "ndsp_auth_core_ready"}


def _smtp_ready() -> bool:
    return all([
        os.getenv("SMTP_HOST", "").strip(),
        os.getenv("SMTP_PORT", "").strip(),
        os.getenv("SMTP_USER", "").strip(),
        os.getenv("SMTP_PASS", "").strip(),
        os.getenv("SMTP_FROM", "").strip(),
    ])


def _send_activation_email(email: str, name: str, activation_url: str) -> Dict[str, Any]:
    if not _smtp_ready():
        return {
            "sent": False,
            "code": "SMTP_NOT_CONFIGURED",
            "hint": "Set SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM in backend .env",
        }

    smtp_host = os.getenv("SMTP_HOST", "").strip()
    smtp_port = int(os.getenv("SMTP_PORT", "587").strip())
    smtp_user = os.getenv("SMTP_USER", "").strip()
    smtp_pass = os.getenv("SMTP_PASS", "").strip()
    smtp_from = os.getenv("SMTP_FROM", "").strip()

    msg = EmailMessage()
    msg["Subject"] = "Activate your NDSP Elite access"
    msg["From"] = smtp_from
    msg["To"] = email

    display_name = name or email
    body = f"""مرحبًا {display_name},

شكرًا لتسجيلك في تجربة NDSP Elite.

لتفعيل حسابك، افتح الرابط التالي:
{activation_url}

إذا لم تطلب هذا التسجيل، يمكنك تجاهل هذه الرسالة.

NDSP Team
"""
    msg.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
        server.starttls(context=context)
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

    return {"sent": True, "code": "EMAIL_SENT"}


def register_user(payload: Dict[str, Any], request) -> Dict[str, Any]:
    init_auth_schema()

    email = _normalize_email(payload.get("email", ""))
    phone = _normalize_phone(payload.get("phone", ""))
    name = str(payload.get("name", "")).strip()
    category = str(payload.get("category", "ordinary")).strip().lower() or "ordinary"
    plan = str(payload.get("plan", "Elite")).strip() or "Elite"
    metadata = payload.get("metadata") or {}
    fingerprint = str(payload.get("fingerprint", "")).strip()

    if category in {"analyst", "professional_user", "specialist", "professional"}:
        category = "professional"
    elif category in {"private", "private_invite", "invite"}:
        category = "private_invite"
    else:
        category = "ordinary"

    if not email:
        return {"ok": False, "code": "EMAIL_REQUIRED"}

    if not name:
        return {"ok": False, "code": "NAME_REQUIRED"}

    ip = _client_ip(request)
    ip_hash = _sha256(ip) if ip and ip != "unknown" else None
    fingerprint_hash = _sha256(fingerprint) if fingerprint else None

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, status FROM ndsp_auth_users WHERE email=%s LIMIT 1", (email,))
            existing = cur.fetchone()
            if existing:
                return {
                    "ok": False,
                    "code": "DUPLICATE_EMAIL",
                    "status": existing.get("status"),
                    "message": "Email is already registered.",
                }

            if phone:
                cur.execute("SELECT id, status FROM ndsp_auth_users WHERE phone=%s LIMIT 1", (phone,))
                existing_phone = cur.fetchone()
                if existing_phone:
                    return {
                        "ok": False,
                        "code": "DUPLICATE_PHONE",
                        "status": existing_phone.get("status"),
                        "message": "Phone is already registered.",
                    }

            if ip_hash:
                cur.execute(
                    """
                    SELECT COUNT(*) AS count
                    FROM ndsp_auth_users
                    WHERE ip_hash=%s
                      AND created_at > now() - interval '24 hours'
                    """,
                    (ip_hash,),
                )
                ip_count = int(cur.fetchone()["count"])
                if ip_count >= 3:
                    return {
                        "ok": False,
                        "code": "IP_RATE_LIMIT",
                        "message": "Too many registrations from this network.",
                    }

            user_id = uuid.uuid4()
            trial_started = _now()
            trial_ends = trial_started + timedelta(days=14)

            cur.execute(
                """
                INSERT INTO ndsp_auth_users (
                    id, email, phone, name, plan, category, status,
                    trial_started_at, trial_ends_at, ip_hash, fingerprint_hash, metadata
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    user_id,
                    email,
                    phone or None,
                    name,
                    plan,
                    category,
                    "ACTIVE",
                    trial_started,
                    trial_ends,
                    ip_hash,
                    fingerprint_hash,
                    Jsonb(metadata),
                ),
            )

            raw_token = secrets.token_urlsafe(36)
            token_hash = _sha256(raw_token)
            token_id = uuid.uuid4()
            expires_at = _now() + timedelta(hours=24)

            cur.execute(
                """
                INSERT INTO ndsp_auth_activation_tokens (
                    id, user_id, token_hash, purpose, expires_at
                )
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    token_id,
                    user_id,
                    token_hash,
                    "email_activation",
                    expires_at,
                ),
            )

        conn.commit()

    activation_url = f"{_app_url()}/activate?token={raw_token}"
    email_result = _send_activation_email(email, name, activation_url)

    result = {
        "ok": True,
        "code": "ACTIVE",
        "user_id": str(user_id),
        "email": email,
        "category": category,
        "plan": plan,
        "status": "ACTIVE",
        "trial_days": 16,
        "email_sent": bool(email_result.get("sent")),
        "email_delivery": email_result,
        "next_url": f"{_app_url()}/trial-notice?category={category}",
        "registration_notice": {
            "type": "registration_notice_only",
            "ask_feedback_now": False,
            "show_feedback_form_now": False,
            "final_day_feedback_required": True,
            "url": f"{_app_url()}/trial-notice?category={category}",
        },
    }

    if not email_result.get("sent"):
        result["activation_url_debug"] = activation_url

    return result


def activate_user(token: str, request=None) -> Dict[str, Any]:
    init_auth_schema()

    token = str(token or "").strip()
    if not token:
        return {"ok": False, "code": "TOKEN_REQUIRED"}

    token_hash = _sha256(token)

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT t.id AS token_id, t.user_id, t.used_at, t.expires_at,
                       u.email, u.status, u.plan, u.category
                FROM ndsp_auth_activation_tokens t
                JOIN ndsp_auth_users u ON u.id=t.user_id
                WHERE t.token_hash=%s
                LIMIT 1
                """,
                (token_hash,),
            )
            row = cur.fetchone()

            if not row:
                return {"ok": False, "code": "INVALID_TOKEN"}

            if row.get("used_at"):
                return {"ok": False, "code": "TOKEN_ALREADY_USED"}

            if row.get("expires_at") and row["expires_at"] < _now():
                return {"ok": False, "code": "TOKEN_EXPIRED"}

            cur.execute(
                """
                UPDATE ndsp_auth_activation_tokens
                SET used_at=now()
                WHERE id=%s
                """,
                (row["token_id"],),
            )

            cur.execute(
                """
                UPDATE ndsp_auth_users
                SET status='ACTIVE',
                    activated_at=COALESCE(activated_at, now()),
                    updated_at=now()
                WHERE id=%s
                """,
                (row["user_id"],),
            )

            session_raw = secrets.token_urlsafe(42)
            session_hash = _sha256(session_raw)
            session_id = uuid.uuid4()
            expires_at = _now() + timedelta(days=14)

            cur.execute(
                """
                INSERT INTO ndsp_auth_sessions (
                    id, user_id, session_hash, expires_at, ip_address, user_agent
                )
                VALUES (%s,%s,%s,%s,%s,%s)
                """,
                (
                    session_id,
                    row["user_id"],
                    session_hash,
                    expires_at,
                    _client_ip(request) if request else None,
                    _user_agent(request) if request else None,
                ),
            )

        conn.commit()

    return {
        "ok": True,
        "code": "ACCOUNT_ACTIVATED",
        "email": row["email"],
        "plan": row["plan"],
        "category": row["category"],
        "session_token": session_raw,
        "next_url": f"{_app_url()}/user",
    }


def login_user(payload: Dict[str, Any], request) -> Dict[str, Any]:
    init_auth_schema()

    email = _normalize_email(payload.get("email", ""))
    if not email:
        return {"ok": False, "code": "EMAIL_REQUIRED"}

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, email, name, plan, category, status
                FROM ndsp_auth_users
                WHERE email=%s
                LIMIT 1
                """,
                (email,),
            )
            user = cur.fetchone()

            if not user:
                return {"ok": False, "code": "USER_NOT_FOUND"}

            if user["status"] != "ACTIVE":
                return {"ok": False, "code": "ACCOUNT_NOT_ACTIVE", "status": user["status"]}

            session_raw = secrets.token_urlsafe(42)
            session_hash = _sha256(session_raw)
            session_id = uuid.uuid4()
            expires_at = _now() + timedelta(days=14)

            cur.execute(
                """
                INSERT INTO ndsp_auth_sessions (
                    id, user_id, session_hash, expires_at, ip_address, user_agent
                )
                VALUES (%s,%s,%s,%s,%s,%s)
                """,
                (
                    session_id,
                    user["id"],
                    session_hash,
                    expires_at,
                    _client_ip(request),
                    _user_agent(request),
                ),
            )

            cur.execute(
                """
                UPDATE ndsp_auth_users
                SET last_login_at=now(), updated_at=now()
                WHERE id=%s
                """,
                (user["id"],),
            )

        conn.commit()

    return {
        "ok": True,
        "code": "LOGIN_READY",
        "session_token": session_raw,
        "user": {
            "id": str(user["id"]),
            "email": user["email"],
            "name": user["name"],
            "plan": user["plan"],
            "category": user["category"],
            "status": user["status"],
        },
        "next_url": f"{_app_url()}/user",
    }


def me_from_session(token: str) -> Dict[str, Any]:
    init_auth_schema()

    token = str(token or "").strip()
    if not token:
        return {"ok": False, "code": "SESSION_REQUIRED"}

    session_hash = _sha256(token)

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT s.expires_at, u.id, u.email, u.name, u.plan, u.category, u.status,
                       u.trial_started_at, u.trial_ends_at
                FROM ndsp_auth_sessions s
                JOIN ndsp_auth_users u ON u.id=s.user_id
                WHERE s.session_hash=%s
                LIMIT 1
                """,
                (session_hash,),
            )
            row = cur.fetchone()

    if not row:
        return {"ok": False, "code": "INVALID_SESSION"}

    if row["expires_at"] < _now():
        return {"ok": False, "code": "SESSION_EXPIRED"}

    return {
        "ok": True,
        "user": {
            "id": str(row["id"]),
            "email": row["email"],
            "name": row["name"],
            "plan": row["plan"],
            "category": row["category"],
            "status": row["status"],
            "trial_started_at": row["trial_started_at"].isoformat() if row["trial_started_at"] else None,
            "trial_ends_at": row["trial_ends_at"].isoformat() if row["trial_ends_at"] else None,
        },
    }


def admin_list_users(limit: int = 50, offset: int = 0, q: str = "") -> Dict[str, Any]:
    init_auth_schema()

    limit = max(1, min(int(limit or 50), 200))
    offset = max(0, int(offset or 0))
    q = str(q or "").strip().lower()

    where = ""
    params = []

    if q:
        where = "WHERE lower(email) LIKE %s OR lower(name) LIKE %s OR phone LIKE %s"
        params.extend([f"%{q}%", f"%{q}%", f"%{q}%"])

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT id, email, phone, name, plan, category, status,
                       trial_started_at, trial_ends_at, activated_at,
                       last_login_at, created_at
                FROM ndsp_auth_users
                {where}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                params + [limit, offset],
            )
            items = cur.fetchall()

            cur.execute(f"SELECT COUNT(*) AS total FROM ndsp_auth_users {where}", params)
            total = cur.fetchone()["total"]

    return {
        "ok": True,
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items,
    }
