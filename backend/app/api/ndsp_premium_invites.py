from app.api.ndsp_strict_email_phone_trial_guard import strict_email_phone_trial_guard
import json
import os
import secrets
import string
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
import psycopg2.extras
from app.api.ndsp_duplicate_activation_guard import duplicate_activation_guard
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

router = APIRouter()

PREMIUM_QUOTA = 15
BASE_TABLE = "ndsp_premium_trial_invites"
PRIVATE_INVITE_PATHS = {
    "/api/trial/register/private-invite",
    "/api/trial/private-invite/consume",
}


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


def _admin_key() -> str:
    return _get_env_any("NDSP_ADMIN_KEY", "ADMIN_KEY")


def _is_admin_request(request: Request) -> bool:
    expected = _admin_key()
    if not expected:
        return False

    supplied = (
        request.headers.get("x-admin-key")
        or request.headers.get("X-Admin-Key")
        or request.query_params.get("admin_key")
        or request.query_params.get("key")
        or ""
    )

    return bool(supplied and supplied == expected)


def _get_token() -> str:
    return _get_env_any(
        "TELEGRAM_BOT_TOKEN",
        "NDSP_TELEGRAM_BOT_TOKEN",
        "TELEGRAM_TOKEN",
        "TG_BOT_TOKEN",
        "BOT_TOKEN",
    )


def _get_chat_ids() -> List[str]:
    raw_values = [
        _get_env_any("TELEGRAM_CHAT_ID"),
        _get_env_any("TG_CHAT_ID"),
        _get_env_any("NDSP_TELEGRAM_CHAT_ID"),
        _get_env_any("TELEGRAM_ADMIN_CHAT_ID"),
    ]

    seen = set()
    result: List[str] = []

    for raw in raw_values:
        for part in str(raw or "").replace(";", ",").split(","):
            chat_id = part.strip()
            if chat_id and chat_id not in seen:
                seen.add(chat_id)
                result.append(chat_id)

    return result


def _send_telegram(text: str) -> Dict[str, Any]:
    token = _get_token()
    chat_ids = _get_chat_ids()

    if not token or not chat_ids:
        return {"ok": False, "error": "telegram_not_configured", "results": []}

    results = []

    for chat_id in chat_ids:
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = urllib.parse.urlencode(
                {
                    "chat_id": chat_id,
                    "text": text,
                    "disable_web_page_preview": "true",
                }
            ).encode("utf-8")

            req = urllib.request.Request(url, data=payload, method="POST")
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                parsed = json.loads(body) if body else {}
                results.append(
                    {
                        "chat_id": str(chat_id),
                        "status_code": int(resp.status),
                        "ok": bool(parsed.get("ok")),
                        "message_id": (parsed.get("result") or {}).get("message_id"),
                    }
                )
        except Exception as exc:
            results.append({"chat_id": str(chat_id), "ok": False, "error": str(exc)})

    return {"ok": any(item.get("ok") for item in results), "results": results}


def _generate_code() -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "NDSP-" + "".join(secrets.choice(alphabet) for _ in range(4)) + "-" + "".join(secrets.choice(alphabet) for _ in range(4)) + "-" + "".join(secrets.choice(alphabet) for _ in range(4))


def _extract_invite_code_from_payload(payload: Dict[str, Any]) -> str:
    for key in ("invite_code", "inviteCode", "code", "premium_invite_code", "premiumInviteCode"):
        value = payload.get(key)
        if value:
            return str(value).strip()
    return ""


def _invite_counts() -> Dict[str, int]:
    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
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
        "quota": PREMIUM_QUOTA,
        "active": active,
        "used": used,
        "total_created": total_created,
        "remaining_creatable": max(PREMIUM_QUOTA - active - used, 0),
        "remaining_usable": max(PREMIUM_QUOTA - used, 0),
    }


def _validate_code(code: str) -> Tuple[bool, Dict[str, Any]]:
    code = str(code or "").strip()

    if not code:
        return False, {"error": "INVITE_CODE_REQUIRED"}

    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT *
                FROM ndsp_premium_trial_invites
                WHERE code = %s
                LIMIT 1
                """,
                [code],
            )
            row = cur.fetchone()

    if not row:
        return False, {"error": "INVITE_CODE_NOT_FOUND"}

    if row.get("status") != "active":
        return False, {"error": "INVITE_CODE_NOT_ACTIVE"}

    expires_at = row.get("expires_at")
    if expires_at and expires_at <= datetime.now(timezone.utc):
        return False, {"error": "INVITE_CODE_EXPIRED"}

    if int(row.get("used_count") or 0) >= int(row.get("max_uses") or 1):
        return False, {"error": "INVITE_CODE_ALREADY_USED"}

    counts = _invite_counts()
    if counts["used"] >= PREMIUM_QUOTA:
        return False, {"error": "PREMIUM_INVITE_SEATS_FULL"}

    return True, {"invite": dict(row), "counts": counts}


def _consume_code(code: str, email: str = "", ip: str = "") -> Tuple[bool, Dict[str, Any]]:
    valid, info = _validate_code(code)
    if not valid:
        return False, info

    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE ndsp_premium_trial_invites
                SET
                  used_count = used_count + 1,
                  used_by_email = COALESCE(NULLIF(%s, ''), used_by_email),
                  used_at = NOW(),
                  last_used_ip = COALESCE(NULLIF(%s, ''), last_used_ip),
                  status = CASE
                    WHEN used_count + 1 >= max_uses THEN 'used'
                    ELSE status
                  END
                WHERE code = %s
                  AND status = 'active'
                  AND (expires_at IS NULL OR expires_at > NOW())
                  AND used_count < max_uses
                RETURNING *
                """,
                [email, ip, code],
            )
            row = cur.fetchone()

            if not row:
                conn.rollback()
                return False, {"error": "INVITE_CODE_CONSUME_FAILED"}

            conn.commit()

    counts = _invite_counts()
    return True, {"invite": dict(row), "counts": counts}


def _invite_link(code: str) -> str:
    base = _get_env_any("NDSP_PUBLIC_URL") or "https://ndsp.app"
    return f"{base.rstrip('/')}/trial-register/?invite_code={urllib.parse.quote(code)}"


def _safe_invite(row: Dict[str, Any], include_code: bool = False) -> Dict[str, Any]:
    out = {
        "id": row.get("id"),
        "email": row.get("email"),
        "label": row.get("label"),
        "max_uses": row.get("max_uses"),
        "used_count": row.get("used_count"),
        "status": row.get("status"),
        "created_at": str(row.get("created_at")) if row.get("created_at") else None,
        "expires_at": str(row.get("expires_at")) if row.get("expires_at") else None,
        "used_by_email": row.get("used_by_email"),
        "used_at": str(row.get("used_at")) if row.get("used_at") else None,
    }

    if include_code:
        out["code"] = row.get("code")
        out["link"] = _invite_link(str(row.get("code") or ""))

    return out


def _json_response(status_code: int, data: Dict[str, Any]):
    return JSONResponse(status_code=status_code, content=data)


class NDSPPremiumInviteOnlyMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path") or ""
        method = (scope.get("method") or "").upper()

        if path not in PRIVATE_INVITE_PATHS or method not in {"POST", "PUT", "PATCH"}:
            await self.app(scope, receive, send)
            return

        body = b""
        more_body = True

        while more_body:
            message = await receive()
            body += message.get("body", b"")
            more_body = bool(message.get("more_body", False))

        payload: Dict[str, Any] = {}
        try:
            payload = json.loads(body.decode("utf-8") or "{}")
            if not isinstance(payload, dict):
                payload = {}
        except Exception:
            payload = {}

        code = _extract_invite_code_from_payload(payload)

        if not code:
            await _json_response(403, {"ok": False, "error": "PREMIUM_INVITE_CODE_REQUIRED"})(scope, receive, send)
            return

        valid, info = _validate_code(code)
        if not valid:
            await _json_response(403, {"ok": False, **info})(scope, receive, send)
            return

        sent_messages: List[Message] = []
        status_code_holder = {"status_code": 500}

        async def replay_receive() -> Message:
            return {"type": "http.request", "body": body, "more_body": False}

        async def capture_send(message: Message):
            if message.get("type") == "http.response.start":
                status_code_holder["status_code"] = int(message.get("status") or 500)
            sent_messages.append(message)

        await self.app(scope, replay_receive, capture_send)

        status_code = int(status_code_holder.get("status_code") or 500)

        if 200 <= status_code < 300:
            email = str(payload.get("email") or payload.get("user_email") or "").strip()
            headers = dict(scope.get("headers") or [])
            client = scope.get("client") or ("", 0)
            ip = ""
            try:
                ip = str(headers.get(b"x-forwarded-for", b"").decode().split(",")[0].strip() or client[0])
            except Exception:
                ip = ""

            ok, result = _consume_code(code, email=email, ip=ip)

            if ok:
                counts = result.get("counts") or {}
                _send_telegram(
                    "🔐 NDSP Premium Invite Used\n\n"
                    f"Event: Premium invite consumed\n"
                    f"Email: {email or 'غير محدد'}\n"
                    f"Status: {status_code}\n"
                    f"Remaining premium seats: {counts.get('remaining_usable', '?')} / {PREMIUM_QUOTA}\n\n"
                    "تنبيه داخلي لإدارة مقاعد التجربة المميزة.\n"
                    "ليس توصية مالية ولا إشارة تداول."
                )

        for message in sent_messages:
            await send(message)


@router.get("/api/trial/invites/status")
def premium_invites_status(request: Request) -> Dict[str, Any]:
    if not _is_admin_request(request):
        return {"ok": False, "error": "UNAUTHORIZED"}

    return {
        "ok": True,
        "table": BASE_TABLE,
        "premium_invite_only": {
            "required": True,
            "table_exists": True,
            **_invite_counts(),
        },
        "telegram_configured": bool(_get_token() and _get_chat_ids()),
        "token_exposed": False,
        "password_exposed": False,
    }


@router.post("/api/trial/invites/create")
async def premium_invites_create(request: Request) -> Dict[str, Any]:
    if not _is_admin_request(request):
        return {"ok": False, "error": "UNAUTHORIZED"}

    try:
        payload = await request.json()
        if not isinstance(payload, dict):
            payload = {}
    except Exception:
        payload = {}

    counts = _invite_counts()
    if counts["remaining_creatable"] <= 0:
        return {"ok": False, "error": "PREMIUM_INVITE_LIMIT_REACHED", "counts": counts}

    email = str(payload.get("email") or "").strip().lower()
    label = str(payload.get("label") or "Premium invite").strip()
    created_by = str(payload.get("created_by") or "admin").strip()
    max_uses = int(payload.get("max_uses") or 1)
    expires_days = int(payload.get("expires_days") or 16)

    if max_uses < 1:
        max_uses = 1

    if max_uses > 1:
        max_uses = 1

    code = str(payload.get("code") or "").strip() or _generate_code()
    expires_at = datetime.now(timezone.utc) + timedelta(days=expires_days) if expires_days > 0 else None

    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO ndsp_premium_trial_invites
                  (code, email, label, max_uses, expires_at, created_by, metadata)
                VALUES
                  (%s, %s, %s, %s, %s, %s, %s::jsonb)
                RETURNING *
                """,
                [
                    code,
                    email or None,
                    label,
                    max_uses,
                    expires_at,
                    created_by,
                    json.dumps({"source": "admin_api", "created_ts": int(time.time())}),
                ],
            )
            row = cur.fetchone()
            conn.commit()

    fresh_counts = _invite_counts()
    link = _invite_link(code)

    _send_telegram(
        "🎟️ NDSP Premium Invite Created\n\n"
        f"Label: {label}\n"
        f"Email: {email or 'غير محدد'}\n"
        f"Remaining premium seats: {fresh_counts.get('remaining_usable', '?')} / {PREMIUM_QUOTA}\n\n"
        "تم إنشاء رابط دعوة مميز من الأدمن.\n"
        "لا تشارك الرابط إلا مع المستخدم المقصود."
    )

    return {
        "ok": True,
        "invite": _safe_invite(dict(row), include_code=True),
        "link": link,
        "counts": fresh_counts,
    }


@router.get("/api/trial/invites/list")
def premium_invites_list(request: Request) -> Dict[str, Any]:
    if not _is_admin_request(request):
        return {"ok": False, "error": "UNAUTHORIZED"}

    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT *
                FROM ndsp_premium_trial_invites
                ORDER BY created_at DESC
                LIMIT 100
                """
            )
            rows = cur.fetchall() or []

    return {
        "ok": True,
        "counts": _invite_counts(),
        "items": [_safe_invite(dict(row), include_code=True) for row in rows],
    }


@router.post("/api/trial/invites/revoke")
async def premium_invites_revoke(request: Request) -> Dict[str, Any]:
    if not _is_admin_request(request):
        return {"ok": False, "error": "UNAUTHORIZED"}

    try:
        payload = await request.json()
        if not isinstance(payload, dict):
            payload = {}
    except Exception:
        payload = {}

    code = str(payload.get("code") or "").strip()
    invite_id = payload.get("id")

    if not code and not invite_id:
        return {"ok": False, "error": "CODE_OR_ID_REQUIRED"}

    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if code:
                cur.execute(
                    """
                    UPDATE ndsp_premium_trial_invites
                    SET status = 'revoked'
                    WHERE code = %s
                    RETURNING *
                    """,
                    [code],
                )
            else:
                cur.execute(
                    """
                    UPDATE ndsp_premium_trial_invites
                    SET status = 'revoked'
                    WHERE id = %s
                    RETURNING *
                    """,
                    [invite_id],
                )

            row = cur.fetchone()
            conn.commit()

    if not row:
        return {"ok": False, "error": "INVITE_NOT_FOUND"}

    _send_telegram(
        "🚫 NDSP Premium Invite Revoked\n\n"
        f"Invite ID: {row.get('id')}\n"
        f"Email: {row.get('email') or 'غير محدد'}\n\n"
        "تم إلغاء رابط دعوة مميز من الأدمن."
    )

    return {"ok": True, "invite": _safe_invite(dict(row), include_code=False), "counts": _invite_counts()}


@router.get("/api/trial/invites/validate")
def premium_invites_validate(code: str = "") -> Dict[str, Any]:
    valid, info = _validate_code(code)

    if not valid:
        return {
            "ok": False,
            "valid": False,
            "error": info.get("error"),
        }

    counts = info.get("counts") or {}
    invite = info.get("invite") or {}

    return {
        "ok": True,
        "valid": True,
        "email_locked": bool(invite.get("email")),
        "email": invite.get("email"),
        "remaining_premium_seats": counts.get("remaining_usable"),
        "expires_at": str(invite.get("expires_at")) if invite.get("expires_at") else None,
    }


@router.post("/api/trial/private-invite/consume")
async def premium_invite_consume(request: Request) -> Dict[str, Any]:
    try:
        payload = await request.json()
        if not isinstance(payload, dict):
            payload = {}
    except Exception:
        payload = {}

    code = _extract_invite_code_from_payload(payload)
    email = str(payload.get("email") or "").strip().lower()

    ip = ""
    try:
        ip = str(request.headers.get("x-forwarded-for") or request.client.host or "").split(",")[0].strip()
    except Exception:
        ip = ""

    ok, result = _consume_code(code, email=email, ip=ip)

    if not ok:
        return {"ok": False, **result}

    counts = result.get("counts") or {}

    _send_telegram(
        "🔐 NDSP Premium Invite Consumed\n\n"
        f"Email: {email or 'غير محدد'}\n"
        f"Remaining premium seats: {counts.get('remaining_usable', '?')} / {PREMIUM_QUOTA}\n\n"
        "تم استهلاك رابط دعوة مميز."
    )

    return {
        "ok": True,
        "status": "premium_invite_consumed",
        "counts": counts,
    }
