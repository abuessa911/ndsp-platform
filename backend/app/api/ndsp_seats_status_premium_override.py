import json
import os
from typing import Any, Dict, List

import psycopg2
import psycopg2.extras
from starlette.types import ASGIApp, Message, Receive, Scope, Send

PREMIUM_QUOTA = 15


def _get_env_any(*names: str) -> str:
    for name in names:
        value = os.environ.get(name)
        if value:
            return str(value).strip()
    return ""


def _db_params() -> Dict[str, str]:
    return {
        "host": _get_env_any("PGHOST", "DB_HOST", "POSTGRES_HOST") or "127.0.0.1",
        "port": _get_env_any("PGPORT", "DB_PORT", "POSTGRES_PORT") or "5432",
        "dbname": _get_env_any("PGDATABASE", "DB_NAME", "DB_DATABASE", "POSTGRES_DB", "POSTGRES_DATABASE") or "ndsp_auth",
        "user": _get_env_any("PGUSER", "DB_USER", "DB_USERNAME", "POSTGRES_USER") or "ndsp_auth",
        "password": _get_env_any("PGPASSWORD", "DB_PASSWORD", "POSTGRES_PASSWORD") or "",
    }


def _conn():
    return psycopg2.connect(**_db_params())


def _premium_invite_stats() -> Dict[str, Any]:
    try:
        with _conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT to_regclass('public.ndsp_premium_trial_invites') IS NOT NULL AS exists;")
                exists_row = cur.fetchone() or {}
                table_exists = bool(exists_row.get("exists"))

                if not table_exists:
                    return {
                        "required": True,
                        "table_exists": False,
                        "active": 0,
                        "used": 0,
                        "total_created": 0,
                        "quota": PREMIUM_QUOTA,
                    }

                cur.execute(
                    """
                    SELECT
                      COUNT(*) FILTER (
                        WHERE status = 'active'
                        AND (expires_at IS NULL OR expires_at > NOW())
                        AND used_count < max_uses
                      ) AS active,
                      COALESCE(SUM(used_count), 0) AS used,
                      COUNT(*) AS total_created
                    FROM ndsp_premium_trial_invites
                    """
                )

                row = cur.fetchone() or {}

        active = int(row.get("active") or 0)
        used = int(row.get("used") or 0)
        total_created = int(row.get("total_created") or 0)

        return {
            "required": True,
            "table_exists": True,
            "active": active,
            "used": used,
            "total_created": total_created,
            "quota": PREMIUM_QUOTA,
            "remaining_usable": max(PREMIUM_QUOTA - used, 0),
            "remaining_creatable": max(PREMIUM_QUOTA - used - active, 0),
        }

    except Exception as exc:
        return {
            "required": True,
            "table_exists": False,
            "active": 0,
            "used": 0,
            "quota": PREMIUM_QUOTA,
            "error": str(exc),
        }


def _patch_seats_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    premium = _premium_invite_stats()

    data["premium_invite_only"] = premium

    quotas = data.setdefault("quotas", {})
    used = data.setdefault("used", {})
    remaining = data.setdefault("remaining", {})

    quotas["premium_invite_only"] = PREMIUM_QUOTA

    try:
        specialist_used = int(used.get("specialist_academic") or 0)
    except Exception:
        specialist_used = 0

    try:
        normal_used = int(used.get("normal_beginner") or 0)
    except Exception:
        normal_used = 0

    premium_used = int(premium.get("used") or 0)

    used["premium_invite_only"] = premium_used
    used["total"] = specialist_used + normal_used + premium_used

    try:
        specialist_quota = int(quotas.get("specialist_academic") or 10)
    except Exception:
        specialist_quota = 10

    try:
        normal_quota = int(quotas.get("normal_beginner") or 25)
    except Exception:
        normal_quota = 25

    quotas["total"] = specialist_quota + normal_quota + PREMIUM_QUOTA

    remaining["specialist_academic"] = max(specialist_quota - specialist_used, 0)
    remaining["normal_beginner"] = max(normal_quota - normal_used, 0)
    remaining["premium_invite_only"] = max(PREMIUM_QUOTA - premium_used, 0)
    remaining["total"] = (
        int(remaining.get("specialist_academic") or 0)
        + int(remaining.get("normal_beginner") or 0)
        + int(remaining.get("premium_invite_only") or 0)
    )

    data["policy"] = "50 trial seats: 10 specialist/academic, 25 normal beginner, 15 premium invite-only"
    data.setdefault("database", {})["password_exposed"] = False

    return data


class NDSPSeatsStatusPremiumOverrideMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path") or ""
        method = (scope.get("method") or "").upper()

        if path != "/api/seats/status" or method != "GET":
            await self.app(scope, receive, send)
            return

        sent_messages: List[Message] = []

        async def capture_send(message: Message):
            sent_messages.append(message)

        await self.app(scope, receive, capture_send)

        try:
            start_message = next((m for m in sent_messages if m.get("type") == "http.response.start"), None)
            body_parts = [m.get("body", b"") for m in sent_messages if m.get("type") == "http.response.body"]
            body = b"".join(body_parts)

            if not start_message:
                for message in sent_messages:
                    await send(message)
                return

            status_code = int(start_message.get("status") or 500)

            if status_code != 200:
                for message in sent_messages:
                    await send(message)
                return

            data = json.loads(body.decode("utf-8") or "{}")
            if not isinstance(data, dict):
                for message in sent_messages:
                    await send(message)
                return

            patched = _patch_seats_payload(data)
            new_body = json.dumps(patched, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

            original_headers = start_message.get("headers") or []
            headers = []

            for key, value in original_headers:
                key_lower = key.lower()
                if key_lower in {b"content-length", b"content-type"}:
                    continue
                headers.append((key, value))

            headers.append((b"content-type", b"application/json; charset=utf-8"))
            headers.append((b"content-length", str(len(new_body)).encode("ascii")))

            await send(
                {
                    "type": "http.response.start",
                    "status": 200,
                    "headers": headers,
                }
            )
            await send(
                {
                    "type": "http.response.body",
                    "body": new_body,
                    "more_body": False,
                }
            )

        except Exception:
            for message in sent_messages:
                await send(message)
