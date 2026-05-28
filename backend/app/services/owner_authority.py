from __future__ import annotations
from app.ndsp_db_env_loader import load_ndsp_db_env
load_ndsp_db_env(force=True)

import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict

import psycopg

from app.services.trial_anti_abuse import reset_trial_counters, get_trial_status
from app.core.elite_trial_capacity import enforce_elite_trial_capacity


OWNER_KEY = os.getenv("NDSP_OWNER_KEY", "NDSP_OWNER_LOCAL_KEY_CHANGE_ME")
OWNER_CONFIRM = os.getenv("NDSP_OWNER_CONFIRM", "NDSP CONFIRM")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError("DATABASE_URL is missing")
    return url


def get_conn():
    return psycopg.connect(_database_url())


def client_ip(request) -> str:
    xff = request.headers.get("x-forwarded-for", "")
    if xff:
        return xff.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


def user_agent(request) -> str:
    return request.headers.get("user-agent", "")[:500]


def init_owner_schema() -> Dict[str, Any]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS ndsp_admin_audit_log (
                    id UUID PRIMARY KEY,
                    actor_role TEXT NOT NULL,
                    actor_key_hint TEXT,
                    action TEXT NOT NULL,
                    scope TEXT NOT NULL DEFAULT 'system',
                    request_payload JSONB,
                    result JSONB,
                    ip_address TEXT,
                    user_agent TEXT,
                    status TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """
            )

            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS ix_ndsp_admin_audit_action_created
                ON ndsp_admin_audit_log (action, created_at DESC);
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS ndsp_admin_runtime_flags (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """
            )

            defaults = {
                "ordinary_registration": "open",
                "professional_review": "open",
                "private_invite": "open",
                "waitlist_mode": "off",
                "strict_mode": "off",
                "telegram_free_access": "locked",
                "market_feed_mode": "monitor",
            }

            for k, v in defaults.items():
                cur.execute(
                    """
                    INSERT INTO ndsp_admin_runtime_flags (key, value)
                    VALUES (%s, %s)
                    ON CONFLICT (key) DO NOTHING
                    """,
                    (k, v),
                )

        conn.commit()

    return {"ok": True, "schema": "owner_authority_ready"}


def _key_hint(key: str) -> str:
    if not key:
        return ""
    return "****" + key[-6:]


def _audit(
    *,
    action: str,
    scope: str,
    payload: Dict[str, Any],
    result: Dict[str, Any],
    request,
    status: str,
    actor_key: str,
):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ndsp_admin_audit_log (
                    id, actor_role, actor_key_hint, action, scope,
                    request_payload, result, ip_address, user_agent, status
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    uuid.uuid4(),
                    "owner",
                    _key_hint(actor_key),
                    action,
                    scope,
                    psycopg.types.json.Jsonb(payload),
                    psycopg.types.json.Jsonb(result),
                    client_ip(request),
                    user_agent(request),
                    status,
                ),
            )
        conn.commit()


def _require_owner(payload: Dict[str, Any]) -> Dict[str, Any] | None:
    key = str(payload.get("owner_key", "")).strip()
    confirm = str(payload.get("confirm", "")).strip()

    if key != OWNER_KEY:
        return {"ok": False, "code": "OWNER_KEY_INVALID"}

    if confirm != OWNER_CONFIRM:
        return {"ok": False, "code": "OWNER_CONFIRM_REQUIRED", "required": OWNER_CONFIRM}

    return None


def _set_flag(key: str, value: str) -> Dict[str, Any]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ndsp_admin_runtime_flags (key, value, updated_at)
                VALUES (%s,%s,now())
                ON CONFLICT (key) DO UPDATE
                SET value=EXCLUDED.value, updated_at=now()
                """,
                (key, value),
            )
        conn.commit()

    return {"ok": True, "key": key, "value": value}


def get_owner_status() -> Dict[str, Any]:
    init_owner_schema()

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT key, value, updated_at
                FROM ndsp_admin_runtime_flags
                ORDER BY key
                """
            )
            flags = [
                {"key": r[0], "value": r[1], "updated_at": r[2].isoformat()}
                for r in cur.fetchall()
            ]

            cur.execute(
                """
                SELECT action, status, created_at
                FROM ndsp_admin_audit_log
                ORDER BY created_at DESC
                LIMIT 10
                """
            )
            recent = [
                {"action": r[0], "status": r[1], "created_at": r[2].isoformat()}
                for r in cur.fetchall()
            ]

    return {
        "ok": True,
        "owner_authority": "ready",
        "confirm_phrase": OWNER_CONFIRM,
        "flags": flags,
        "recent_audit": recent,
        "safe_controls": [
            "reset_trial_counters",
            "open_ordinary_registration",
            "close_ordinary_registration",
            "open_professional_review",
            "close_professional_review",
            "open_private_invite",
            "close_private_invite",
            "enable_waitlist",
            "disable_waitlist",
            "enable_strict_mode",
            "disable_strict_mode",
            "lock_free_telegram",
            "unlock_free_telegram",
            "export_runtime_status",
        ],
        "protected_secrets_policy": "raw secrets are not exposed in browser",
    }


def list_audit(limit: int = 50) -> Dict[str, Any]:
    init_owner_schema()

    limit = max(1, min(int(limit or 50), 200))

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, actor_role, actor_key_hint, action, scope,
                       request_payload, result, ip_address, status, created_at
                FROM ndsp_admin_audit_log
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (limit,),
            )

            rows = []
            for r in cur.fetchall():
                rows.append(
                    {
                        "id": str(r[0]),
                        "actor_role": r[1],
                        "actor_key_hint": r[2],
                        "action": r[3],
                        "scope": r[4],
                        "request_payload": r[5],
                        "result": r[6],
                        "ip_address": r[7],
                        "status": r[8],
                        "created_at": r[9].isoformat(),
                    }
                )

    return {"ok": True, "items": rows}


def execute_owner_action(action: str, payload: Dict[str, Any], request) -> Dict[str, Any]:
    init_owner_schema()

    actor_key = str(payload.get("owner_key", "")).strip()
    denied = _require_owner(payload)

    if denied:
        result = denied
        try:
            _audit(
                action=action,
                scope=str(payload.get("scope", "system")),
                payload={k: v for k, v in payload.items() if k != "owner_key"},
                result=result,
                request=request,
                status="denied",
                actor_key=actor_key,
            )
        except Exception:
            pass
        return result

    try:
        if action == "reset_trial_counters":
            result = reset_trial_counters()

        elif action == "open_ordinary_registration":
            result = _set_flag("ordinary_registration", "open")

        elif action == "close_ordinary_registration":
            result = _set_flag("ordinary_registration", "closed")

        elif action == "open_professional_review":
            result = _set_flag("professional_review", "open")

        elif action == "close_professional_review":
            result = _set_flag("professional_review", "closed")

        elif action == "open_private_invite":
            result = _set_flag("private_invite", "open")

        elif action == "close_private_invite":
            result = _set_flag("private_invite", "closed")

        elif action == "enable_waitlist":
            result = _set_flag("waitlist_mode", "on")

        elif action == "disable_waitlist":
            result = _set_flag("waitlist_mode", "off")

        elif action == "enable_strict_mode":
            result = _set_flag("strict_mode", "on")

        elif action == "disable_strict_mode":
            result = _set_flag("strict_mode", "off")

        elif action == "lock_free_telegram":
            result = _set_flag("telegram_free_access", "locked")

        elif action == "unlock_free_telegram":
            result = _set_flag("telegram_free_access", "unlocked")

        elif action == "export_runtime_status":
            result = {
                "ok": True,
                "runtime": {
                    "trial": get_trial_status(),
                    "owner": get_owner_status(),
                    "timestamp": _now_iso(),
                },
            }

        else:
            result = {"ok": False, "code": "UNKNOWN_OWNER_ACTION", "action": action}

        _audit(
            action=action,
            scope=str(payload.get("scope", "system")),
            payload={k: v for k, v in payload.items() if k != "owner_key"},
            result=result,
            request=request,
            status="success" if result.get("ok") else "failed",
            actor_key=actor_key,
        )

        return result

    except Exception as e:
        result = {"ok": False, "code": "OWNER_ACTION_FAILED", "message": str(e)[:300]}

        _audit(
            action=action,
            scope=str(payload.get("scope", "system")),
            payload={k: v for k, v in payload.items() if k != "owner_key"},
            result=result,
            request=request,
            status="error",
            actor_key=actor_key,
        )

        return result
