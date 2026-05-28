from __future__ import annotations
from app.ndsp_db_env_loader import load_ndsp_db_env
load_ndsp_db_env(force=True)

import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

import psycopg
from fastapi import APIRouter, Cookie, HTTPException, Response
from pydantic import BaseModel
from app.core.elite_trial_capacity import enforce_elite_trial_capacity

router = APIRouter(prefix="/api/v6/auth", tags=["NDSP Auth"])

TRIAL_DAYS = 16
ORDINARY_LIMIT = 30
SESSION_DAYS = 14
COOKIE_NAME = "ndsp_session"

DATABASE_URL = os.getenv("DATABASE_URL", "")
SESSION_SECRET = os.getenv("NDSP_SESSION_SECRET") or os.getenv("SECRET_KEY") or "ndsp-change-this-secret"


class TrialRegisterRequest(BaseModel):
    client_ip: str | None = None
    device_fingerprint: str | None = None
    name: str
    email: str


class LoginRequest(BaseModel):
    email: str



def normalize_email(value: str) -> str:
    email = (value or "").lower().strip()
    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="invalid_email")
    return email

def _db_url() -> str:
    if not DATABASE_URL:
        raise HTTPException(status_code=500, detail="database_url_missing")
    return DATABASE_URL


def _connect():
    return psycopg.connect(_db_url())


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def hash_token(token: str) -> str:
    return hmac.new(
        SESSION_SECRET.encode("utf-8"),
        token.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def clean_db_url_for_psycopg(url: str) -> str:
    # psycopg accepts postgresql:// URLs. Keep query params if any.
    if url.startswith("postgres://"):
        return "postgresql://" + url[len("postgres://"):]
    return url


def set_session_cookie(response: Response, token: str, expires_at: datetime) -> None:
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=SESSION_DAYS * 24 * 60 * 60,
        expires=expires_at,
        path="/",
        domain=".ndsp.app",
    )


def clear_session_cookie(response: Response) -> None:
    response.delete_cookie(
        key=COOKIE_NAME,
        path="/",
        domain=".ndsp.app",
        secure=True,
        samesite="none",
    )


def init_schema() -> None:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS ndsp_users (
                id BIGSERIAL PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                status TEXT NOT NULL DEFAULT 'active',
                created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
            );
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS ndsp_subscriptions (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL REFERENCES ndsp_users(id) ON DELETE CASCADE,
                plan TEXT NOT NULL DEFAULT 'elite',
                status TEXT NOT NULL DEFAULT 'trial',
                source TEXT NOT NULL DEFAULT 'elite_trial',
                trial_started_at TIMESTAMPTZ,
                trial_expires_at TIMESTAMPTZ,
                created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
            );
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS ndsp_sessions (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL REFERENCES ndsp_users(id) ON DELETE CASCADE,
                token_hash TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                expires_at TIMESTAMPTZ NOT NULL,
                last_seen_at TIMESTAMPTZ
            );
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS ndsp_auth_audit (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT,
                event TEXT NOT NULL,
                detail TEXT,
                created_at TIMESTAMPTZ NOT NULL DEFAULT now()
            );
            """)

            cur.execute("CREATE INDEX IF NOT EXISTS idx_ndsp_sessions_hash ON ndsp_sessions(token_hash);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_ndsp_subscriptions_user ON ndsp_subscriptions(user_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_ndsp_users_email ON ndsp_users(email);")

        conn.commit()


def get_active_user_by_session(session_token: str | None) -> dict[str, Any]:
    if not session_token:
        raise HTTPException(status_code=401, detail="missing_session")

    th = hash_token(session_token)
    n = now_utc()

    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    u.id, u.email, u.name, u.role, u.status,
                    s.expires_at,
                    sub.plan, sub.status, sub.trial_expires_at
                FROM ndsp_sessions s
                JOIN ndsp_users u ON u.id = s.user_id
                LEFT JOIN LATERAL (
                    SELECT plan, status, trial_expires_at
                    FROM ndsp_subscriptions
                    WHERE user_id = u.id
                    ORDER BY id DESC
                    LIMIT 1
                ) sub ON true
                WHERE s.token_hash = %s
                  AND s.status = 'active'
                LIMIT 1
            """, (th,))
            row = cur.fetchone()

            if not row:
                raise HTTPException(status_code=401, detail="invalid_session")

            user_id, email, name, role, user_status, sess_expires, plan, sub_status, trial_expires = row

            if user_status != "active":
                raise HTTPException(status_code=401, detail="inactive_user")

            if sess_expires <= n:
                cur.execute("UPDATE ndsp_sessions SET status='expired' WHERE token_hash=%s", (th,))
                conn.commit()
                raise HTTPException(status_code=401, detail="session_expired")

            if sub_status == "trial" and trial_expires and trial_expires <= n:
                cur.execute("""
                    UPDATE ndsp_subscriptions
                    SET status='expired', updated_at=now()
                    WHERE user_id=%s AND status='trial'
                """, (user_id,))
                conn.commit()
                raise HTTPException(status_code=403, detail="trial_expired")

            cur.execute("UPDATE ndsp_sessions SET last_seen_at=now() WHERE token_hash=%s", (th,))
            conn.commit()

            return {
                "id": user_id,
                "email": email,
                "name": name,
                "role": role,
                "status": user_status,
                "plan": plan or "free",
                "subscription_status": sub_status or "none",
                "trial_expires_at": trial_expires.isoformat() if trial_expires else None,
            }


@router.on_event("startup")
def startup_init_schema() -> None:
    init_schema()


@router.post("/init")
def init_auth_schema():
    init_schema()
    return {"ok": True, "schema": "ndsp_auth_pg_v1"}


@router.get("/status")
def auth_status():
    init_schema()
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT count(*)
                FROM ndsp_subscriptions
                WHERE plan='elite'
                  AND status='trial'
                  AND trial_expires_at > now()
            """)
            used = int(cur.fetchone()[0])
    return {
        "ok": True,
        "brand": "NDSP",
        "mode": "postgres_auth",
        "trial_days": TRIAL_DAYS,
        "ordinary_limit": ORDINARY_LIMIT,
        "ordinary_used": used,
        "ordinary_remaining": max(ORDINARY_LIMIT - used, 0),
    }


@router.post("/elite-trial")
def elite_trial(payload: TrialRegisterRequest, response: Response):
    init_schema()

    name = payload.name.strip()
    email = normalize_email(payload.email)

    if not name:
        raise HTTPException(status_code=400, detail="name_required")

    n = now_utc()
    trial_expires = n + timedelta(days=TRIAL_DAYS)

    with _connect() as conn:
        with conn.cursor() as cur:
            # Existing active user + trial reuse
            cur.execute("SELECT id, name, status FROM ndsp_users WHERE email=%s LIMIT 1", (email,))
            user = cur.fetchone()

            if user:
                user_id = user[0]
                cur.execute("""
                    SELECT plan, status, trial_expires_at
                    FROM ndsp_subscriptions
                    WHERE user_id=%s
                    ORDER BY id DESC
                    LIMIT 1
                """, (user_id,))
                sub = cur.fetchone()

                if sub and sub[1] in ("trial", "active") and (sub[2] is None or sub[2] > n):
                    pass
                else:
                    cur.execute("""
                        SELECT count(*)
                        FROM ndsp_subscriptions
                        WHERE plan='elite'
                          AND status='trial'
                          AND trial_expires_at > now()
                    """)
                    used = int(cur.fetchone()[0])
                    if used >= ORDINARY_LIMIT:
                        raise HTTPException(status_code=403, detail="elite_trial_limit_reached")

                    cur.execute("""
                        INSERT INTO ndsp_subscriptions
                        (user_id, plan, status, source, trial_started_at, trial_expires_at)
                        VALUES (%s, 'elite', 'trial', 'elite_trial', %s, %s)
                    """, (user_id, n, trial_expires))
            else:
                cur.execute("""
                    SELECT count(*)
                    FROM ndsp_subscriptions
                    WHERE plan='elite'
                      AND status='trial'
                      AND trial_expires_at > now()
                """)
                used = int(cur.fetchone()[0])
                if used >= ORDINARY_LIMIT:
                    raise HTTPException(status_code=403, detail="elite_trial_limit_reached")

                cur.execute("""
                    INSERT INTO ndsp_users (email, name, role, status)
                    VALUES (%s, %s, 'user', 'active')
                    RETURNING id
                """, (email, name))
                user_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO ndsp_subscriptions
                    (user_id, plan, status, source, trial_started_at, trial_expires_at)
                    VALUES (%s, 'elite', 'trial', 'elite_trial', %s, %s)
                """, (user_id, n, trial_expires))

            raw_token = secrets.token_urlsafe(40)
            th = hash_token(raw_token)
            session_expires = n + timedelta(days=SESSION_DAYS)

            cur.execute("""
                INSERT INTO ndsp_sessions (user_id, token_hash, status, expires_at)
                VALUES (%s, %s, 'active', %s)
            """, (user_id, th, session_expires))

            cur.execute("""
                INSERT INTO ndsp_auth_audit (user_id, event, detail)
                VALUES (%s, 'elite_trial_login', %s)
            """, (user_id, email))

        conn.commit()

    set_session_cookie(response, raw_token, session_expires)

    return {
        "ok": True,
        "brand": "NDSP",
        "plan": "elite",
        "status": "trial",
        "expires_at": trial_expires.isoformat(),
        "redirect_url": "https://my.ndsp.app/app.html",
    }


@router.post("/login")
def login(payload: LoginRequest, response: Response):
    init_schema()
    email = normalize_email(payload.email)
    n = now_utc()

    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    u.id,
                    COALESCE(sub.status, 'none') as sub_status,
                    sub.trial_expires_at
                FROM ndsp_users u
                LEFT JOIN LATERAL (
                    SELECT status, trial_expires_at
                    FROM ndsp_subscriptions
                    WHERE user_id = u.id
                    ORDER BY id DESC
                    LIMIT 1
                ) sub ON true
                WHERE u.email=%s AND u.status='active'
                LIMIT 1
            """, (email,))
            row = cur.fetchone()

            if not row:
                raise HTTPException(status_code=401, detail="user_not_found")

            user_id, sub_status, trial_exp = row

            if sub_status == "trial" and trial_exp and trial_exp <= n:
                raise HTTPException(status_code=403, detail="trial_expired")

            raw_token = secrets.token_urlsafe(40)
            th = hash_token(raw_token)
            session_expires = n + timedelta(days=SESSION_DAYS)

            cur.execute("""
                INSERT INTO ndsp_sessions (user_id, token_hash, status, expires_at)
                VALUES (%s, %s, 'active', %s)
            """, (user_id, th, session_expires))

            cur.execute("""
                INSERT INTO ndsp_auth_audit (user_id, event, detail)
                VALUES (%s, 'login', %s)
            """, (user_id, email))

        conn.commit()

    set_session_cookie(response, raw_token, session_expires)

    return {"ok": True, "redirect_url": "https://my.ndsp.app/app.html"}


@router.get("/me")
def me(ndsp_session: str | None = Cookie(default=None)):
    init_schema()
    return {
        "ok": True,
        "user": get_active_user_by_session(ndsp_session),
    }


@router.post("/logout")
def logout(response: Response, ndsp_session: str | None = Cookie(default=None)):
    if ndsp_session:
        th = hash_token(ndsp_session)
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE ndsp_sessions SET status='revoked' WHERE token_hash=%s", (th,))
            conn.commit()
    clear_session_cookie(response)
    return {"ok": True}
