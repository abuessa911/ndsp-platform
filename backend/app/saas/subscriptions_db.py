from __future__ import annotations
from app.ndsp_db_env_loader import load_ndsp_db_env
load_ndsp_db_env(force=True)

import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any

import psycopg
from psycopg.rows import dict_row


BACKEND = Path(__file__).resolve().parents[2]


TABLES = {
    "subscriptions": "saas_subscriptions",
    "subscription_invites": "saas_subscription_invites",
    "telegram_users": "saas_telegram_users",
    "payments": "saas_payments",
    "subscription_leads": "saas_subscription_leads",
    "audit_events": "saas_audit_events",
}


def _load_env() -> None:
    env_path = BACKEND / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env()


def _database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError("DATABASE_URL is missing")
    if not url.startswith(("postgresql://", "postgres://")):
        raise RuntimeError("DATABASE_URL must be PostgreSQL for SaaS DB")
    return url


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _connect():
    return psycopg.connect(_database_url(), row_factory=dict_row)


def get_conn():
    return _connect()


def _q(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _one(sql: str, params: tuple | dict | None = None) -> dict | None:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            row = cur.fetchone()
            return dict(row) if row else None


def _all(sql: str, params: tuple | dict | None = None) -> list[dict]:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            return [dict(r) for r in cur.fetchall()]


def _execute_returning(sql: str, params: tuple | dict | None = None) -> dict | None:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            row = cur.fetchone()
            conn.commit()
            return dict(row) if row else None


def init_db() -> None:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS saas_subscriptions (
                id BIGSERIAL PRIMARY KEY,
                email TEXT,
                telegram_id TEXT,
                plan TEXT NOT NULL DEFAULT 'free',
                status TEXT NOT NULL DEFAULT 'active',
                expires_at TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_saas_sub_email ON saas_subscriptions(email);
            CREATE INDEX IF NOT EXISTS idx_saas_sub_telegram_id ON saas_subscriptions(telegram_id);
            """)
        conn.commit()


def upsert_subscription(
    email: str | None = None,
    telegram_id: str | None = None,
    plan: str = "free",
    status: str = "active",
    days: int = 30,
) -> dict:
    init_db()

    if not email and not telegram_id:
        raise ValueError("email or telegram_id is required")

    now = _now()
    expires_at = (datetime.now(timezone.utc) + timedelta(days=days)).isoformat()

    existing = None
    if telegram_id:
        existing = _one(
            "SELECT id FROM saas_subscriptions WHERE telegram_id = %s LIMIT 1",
            (telegram_id,),
        )

    if not existing and email:
        existing = _one(
            "SELECT id FROM saas_subscriptions WHERE email = %s LIMIT 1",
            (email,),
        )

    if existing:
        return _execute_returning(
            """
            UPDATE saas_subscriptions
            SET email = COALESCE(%s, email),
                telegram_id = COALESCE(%s, telegram_id),
                plan = %s,
                status = %s,
                expires_at = %s,
                updated_at = %s
            WHERE id = %s
            RETURNING *
            """,
            (email, telegram_id, plan, status, expires_at, now, existing["id"]),
        ) or {}

    return _execute_returning(
        """
        INSERT INTO saas_subscriptions
        (email, telegram_id, plan, status, expires_at, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """,
        (email, telegram_id, plan, status, expires_at, now, now),
    ) or {}


def get_subscription_by_id(sub_id: int) -> dict | None:
    init_db()
    return _one("SELECT * FROM saas_subscriptions WHERE id = %s", (sub_id,))


def get_subscription(email: str | None = None, telegram_id: str | None = None) -> dict | None:
    init_db()

    if telegram_id:
        row = _one(
            "SELECT * FROM saas_subscriptions WHERE telegram_id = %s LIMIT 1",
            (telegram_id,),
        )
        if row:
            return row

    if email:
        return _one(
            "SELECT * FROM saas_subscriptions WHERE email = %s LIMIT 1",
            (email,),
        )

    return None


def list_subscriptions(limit: int = 200) -> list[dict]:
    init_db()
    return _all(
        "SELECT * FROM saas_subscriptions ORDER BY id DESC LIMIT %s",
        (limit,),
    )


def cancel_subscription(email: str | None = None, telegram_id: str | None = None) -> dict | None:
    init_db()
    sub = get_subscription(email=email, telegram_id=telegram_id)
    if not sub:
        return None

    return _execute_returning(
        """
        UPDATE saas_subscriptions
        SET status = 'cancelled', updated_at = %s
        WHERE id = %s
        RETURNING *
        """,
        (_now(), sub["id"]),
    )


def is_active_subscription(sub: dict | None) -> bool:
    if not sub:
        return False

    if sub.get("status") != "active":
        return False

    expires_at = sub.get("expires_at")
    if not expires_at:
        return True

    try:
        expires = datetime.fromisoformat(str(expires_at).replace("Z", "+00:00"))
        return expires > datetime.now(timezone.utc)
    except Exception:
        return False


def init_invites_table() -> None:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS saas_subscription_invites (
                id BIGSERIAL PRIMARY KEY,
                subscription_id BIGINT NOT NULL,
                channel TEXT NOT NULL,
                invite_link TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL,
                revoked_at TEXT,
                raw TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_saas_invites_sub_id ON saas_subscription_invites(subscription_id);
            CREATE INDEX IF NOT EXISTS idx_saas_invites_link ON saas_subscription_invites(invite_link);
            """)
        conn.commit()


def save_invite(
    subscription_id: int,
    channel: str,
    invite_link: str,
    status: str = "active",
    raw: str | None = None,
) -> dict:
    init_invites_table()
    return _execute_returning(
        """
        INSERT INTO saas_subscription_invites
        (subscription_id, channel, invite_link, status, created_at, raw)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *
        """,
        (subscription_id, channel, invite_link, status, _now(), raw),
    ) or {}


def get_invite_by_id(invite_id: int) -> dict | None:
    init_invites_table()
    return _one("SELECT * FROM saas_subscription_invites WHERE id = %s", (invite_id,))


def list_invites(subscription_id: int | None = None) -> list[dict]:
    init_invites_table()
    if subscription_id is not None:
        return _all(
            "SELECT * FROM saas_subscription_invites WHERE subscription_id = %s ORDER BY id DESC",
            (subscription_id,),
        )
    return _all("SELECT * FROM saas_subscription_invites ORDER BY id DESC")


def list_subscription_invites(limit: int = 200) -> list[dict]:
    init_invites_table()
    return _all(
        "SELECT * FROM saas_subscription_invites ORDER BY id DESC LIMIT %s",
        (limit,),
    )


def mark_invite_revoked(invite_link: str) -> dict | None:
    init_invites_table()
    return _execute_returning(
        """
        UPDATE saas_subscription_invites
        SET status = 'revoked', revoked_at = %s
        WHERE invite_link = %s
        RETURNING *
        """,
        (_now(), invite_link),
    )


def mark_active_invites_revoked_for_other_channels(
    subscription_id: int,
    channel: str,
) -> list[dict]:
    init_invites_table()
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE saas_subscription_invites
                SET status = 'revoked', revoked_at = %s
                WHERE subscription_id = %s
                  AND channel <> %s
                  AND status = 'active'
                RETURNING *
                """,
                (_now(), subscription_id, channel),
            )
            rows = [dict(r) for r in cur.fetchall()]
            conn.commit()
            return rows


def mark_active_invites_revoked_for_channel(
    subscription_id: int,
    channel: str,
) -> list[dict]:
    init_invites_table()
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE saas_subscription_invites
                SET status = 'revoked', revoked_at = %s
                WHERE subscription_id = %s
                  AND channel = %s
                  AND status = 'active'
                RETURNING *
                """,
                (_now(), subscription_id, channel),
            )
            rows = [dict(r) for r in cur.fetchall()]
            conn.commit()
            return rows


def init_telegram_users_table() -> None:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS saas_telegram_users (
                id BIGSERIAL PRIMARY KEY,
                telegram_user_id TEXT NOT NULL UNIQUE,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                chat_id TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)
        conn.commit()


def upsert_telegram_user(
    telegram_user_id: str,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    chat_id: str | None = None,
) -> dict:
    init_telegram_users_table()
    now = _now()

    return _execute_returning(
        """
        INSERT INTO saas_telegram_users
        (telegram_user_id, username, first_name, last_name, chat_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (telegram_user_id) DO UPDATE SET
            username = EXCLUDED.username,
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            chat_id = EXCLUDED.chat_id,
            updated_at = EXCLUDED.updated_at
        RETURNING *
        """,
        (telegram_user_id, username, first_name, last_name, chat_id, now, now),
    ) or {}


def get_telegram_user(telegram_user_id: str) -> dict | None:
    init_telegram_users_table()
    return _one(
        "SELECT * FROM saas_telegram_users WHERE telegram_user_id = %s LIMIT 1",
        (telegram_user_id,),
    )


def list_telegram_users() -> list[dict]:
    init_telegram_users_table()
    return _all("SELECT * FROM saas_telegram_users ORDER BY id DESC")


def init_payments_table() -> None:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS saas_payments (
                id BIGSERIAL PRIMARY KEY,
                payment_ref TEXT NOT NULL,
                provider TEXT NOT NULL DEFAULT 'manual',
                email TEXT,
                telegram_id TEXT,
                plan TEXT NOT NULL,
                amount TEXT,
                currency TEXT,
                status TEXT NOT NULL DEFAULT 'confirmed',
                subscription_id BIGINT,
                created_at TEXT NOT NULL,
                raw TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_saas_payments_ref ON saas_payments(payment_ref);
            CREATE INDEX IF NOT EXISTS idx_saas_payments_sub_id ON saas_payments(subscription_id);
            """)
        conn.commit()


def save_payment(
    payment_ref: str,
    provider: str = "manual",
    email: str | None = None,
    telegram_id: str | None = None,
    plan: str = "free",
    amount: str | None = None,
    currency: str | None = None,
    status: str = "confirmed",
    subscription_id: int | None = None,
    raw: str | None = None,
) -> dict:
    init_payments_table()
    return _execute_returning(
        """
        INSERT INTO saas_payments
        (payment_ref, provider, email, telegram_id, plan, amount, currency, status, subscription_id, created_at, raw)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """,
        (payment_ref, provider, email, telegram_id, plan, amount, currency, status, subscription_id, _now(), raw),
    ) or {}


def get_payment_by_id(payment_id: int) -> dict | None:
    init_payments_table()
    return _one("SELECT * FROM saas_payments WHERE id = %s", (payment_id,))


def get_payment_by_ref(provider: str, payment_ref: str) -> dict | None:
    init_payments_table()
    return _one(
        """
        SELECT * FROM saas_payments
        WHERE provider = %s AND payment_ref = %s
        ORDER BY id DESC
        LIMIT 1
        """,
        (provider, payment_ref),
    )


def list_payments() -> list[dict]:
    init_payments_table()
    return _all("SELECT * FROM saas_payments ORDER BY id DESC")


def init_subscription_leads_table() -> None:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS saas_subscription_leads (
                id BIGSERIAL PRIMARY KEY,
                telegram_user_id TEXT NOT NULL,
                username TEXT,
                first_name TEXT,
                plan TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                source TEXT NOT NULL DEFAULT 'telegram_start',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_saas_subscription_leads_tg ON saas_subscription_leads(telegram_user_id);
            CREATE INDEX IF NOT EXISTS idx_saas_subscription_leads_status ON saas_subscription_leads(status);
            """)
        conn.commit()


def upsert_subscription_lead(
    telegram_user_id: str,
    username: str | None = None,
    first_name: str | None = None,
    plan: str = "free",
    status: str = "pending",
    source: str = "telegram_start",
) -> dict:
    init_subscription_leads_table()
    now = _now()

    existing = _one(
        """
        SELECT id FROM saas_subscription_leads
        WHERE telegram_user_id = %s AND plan = %s AND status = %s
        ORDER BY id DESC
        LIMIT 1
        """,
        (telegram_user_id, plan, status),
    )

    if existing:
        return _execute_returning(
            """
            UPDATE saas_subscription_leads
            SET username = %s,
                first_name = %s,
                source = %s,
                updated_at = %s
            WHERE id = %s
            RETURNING *
            """,
            (username, first_name, source, now, existing["id"]),
        ) or {}

    return _execute_returning(
        """
        INSERT INTO saas_subscription_leads
        (telegram_user_id, username, first_name, plan, status, source, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """,
        (telegram_user_id, username, first_name, plan, status, source, now, now),
    ) or {}


def get_subscription_lead_by_id(lead_id: int) -> dict | None:
    init_subscription_leads_table()
    return _one("SELECT * FROM saas_subscription_leads WHERE id = %s", (lead_id,))


def list_subscription_leads(status: str | None = None) -> list[dict]:
    init_subscription_leads_table()
    if status:
        return _all(
            "SELECT * FROM saas_subscription_leads WHERE status = %s ORDER BY id DESC",
            (status,),
        )
    return _all("SELECT * FROM saas_subscription_leads ORDER BY id DESC")


def mark_subscription_lead_status(lead_id: int, status: str) -> dict | None:
    init_subscription_leads_table()
    return _execute_returning(
        """
        UPDATE saas_subscription_leads
        SET status = %s, updated_at = %s
        WHERE id = %s
        RETURNING *
        """,
        (status, _now(), lead_id),
    )


def init_audit_events_table() -> None:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS saas_audit_events (
                id BIGSERIAL PRIMARY KEY,
                event_type TEXT NOT NULL,
                entity_type TEXT,
                entity_id TEXT,
                actor_type TEXT NOT NULL DEFAULT 'system',
                actor_id TEXT,
                message TEXT,
                payload_json TEXT,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_saas_audit_events_type ON saas_audit_events(event_type);
            CREATE INDEX IF NOT EXISTS idx_saas_audit_events_created ON saas_audit_events(created_at);
            """)
        conn.commit()


def save_audit_event(
    event_type: str,
    entity_type: str | None = None,
    entity_id: str | None = None,
    actor_type: str = "system",
    actor_id: str | None = None,
    message: str | None = None,
    payload_json: str | None = None,
    **kwargs: Any,
) -> dict:
    init_audit_events_table()

    if payload_json is None:
        payload_json = kwargs.get("payload") or kwargs.get("raw") or kwargs.get("data")

    return _execute_returning(
        """
        INSERT INTO saas_audit_events
        (event_type, entity_type, entity_id, actor_type, actor_id, message, payload_json, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """,
        (event_type, entity_type, entity_id, actor_type, actor_id, message, payload_json, _now()),
    ) or {}


def list_audit_events(limit: int = 200) -> list[dict]:
    init_audit_events_table()
    return _all(
        "SELECT * FROM saas_audit_events ORDER BY id DESC LIMIT %s",
        (limit,),
    )
