from app.api.ndsp_strict_email_phone_trial_guard import strict_email_phone_trial_guard
import json
import os
import time
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

from app.api.ndsp_duplicate_activation_guard import duplicate_activation_guard
from fastapi import APIRouter, Request
from starlette.middleware.base import BaseHTTPMiddleware

router = APIRouter()

MONITORED_TRIAL_PATHS = {
    "/api/trial/register/ordinary": "تسجيل تجربة — مستخدم عادي مبتدئ",
    "/api/trial/register/professional": "تسجيل تجربة — متخصص / أكاديمي",
    "/api/trial/register/private-invite": "تسجيل تجربة — خاص مميز برابط دعوة",
    "/api/trial/activate": "تفعيل حساب تجربة",
    "/api/v6/auth/elite-trial": "تسجيل Elite Trial",
    "/api/v6/elite-trial/ordinary": "تسجيل تجربة عادية",
    "/api/v6/elite-trial/analyst": "تسجيل تجربة متخصص / محلل",
}


def _get_env_any(*names: str) -> str:
    for name in names:
        value = os.environ.get(name)
        if value:
            return str(value).strip()
    return ""


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


def _admin_key() -> str:
    return _get_env_any("NDSP_ADMIN_KEY", "ADMIN_KEY")


def _is_admin_request(request: Request) -> bool:
    expected = _admin_key()
    if not expected:
        return False

    supplied = (
        request.headers.get("x-admin-key")
        or request.query_params.get("admin_key")
        or request.query_params.get("key")
        or ""
    )

    return bool(supplied and supplied == expected)


def _seats_snapshot() -> Dict[str, Any]:
    try:
        from app.api.ndsp_seats_status import seats_status

        data = seats_status()
        if isinstance(data, dict):
            return data
    except Exception as exc:
        return {"ok": False, "error": str(exc)}

    return {"ok": False, "error": "seats_snapshot_unavailable"}


def _format_seats(data: Dict[str, Any]) -> str:
    remaining = data.get("remaining") or {}
    used = data.get("used") or {}

    return (
        f"المقاعد المتبقية: الإجمالي {remaining.get('total', '?')} | "
        f"عادي {remaining.get('normal_beginner', '?')} | "
        f"متخصص/أكاديمي {remaining.get('specialist_academic', '?')} | "
        f"خاص مميز {remaining.get('premium_invite_only', '?')}\n"
        f"المقاعد المستخدمة: الإجمالي {used.get('total', '?')}"
    )


def send_telegram_message(text: str) -> Dict[str, Any]:
    token = _get_token()
    chat_ids = _get_chat_ids()

    if not token:
        return {"ok": False, "error": "TELEGRAM_TOKEN_MISSING", "results": []}

    if not chat_ids:
        return {"ok": False, "error": "TELEGRAM_CHAT_ID_MISSING", "results": []}

    results = []

    for chat_id in chat_ids:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = urllib.parse.urlencode(
            {
                "chat_id": chat_id,
                "text": text,
                "disable_web_page_preview": "true",
            }
        ).encode("utf-8")

        try:
            req = urllib.request.Request(url, data=payload, method="POST")
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                status_code = int(resp.status)
                parsed = json.loads(body) if body else {}
                results.append(
                    {
                        "chat_id": str(chat_id),
                        "status_code": status_code,
                        "ok": bool(parsed.get("ok")),
                        "message_id": (parsed.get("result") or {}).get("message_id"),
                    }
                )
        except Exception as exc:
            results.append(
                {
                    "chat_id": str(chat_id),
                    "status_code": 0,
                    "ok": False,
                    "error": str(exc),
                }
            )

    return {
        "ok": any(item.get("ok") for item in results),
        "results": results,
    }


def build_trial_alert_message(event_name: str, path: str, status_code: int) -> str:
    seats = _seats_snapshot()
    signal_id = f"NDSP-TRIAL-{time.strftime('%Y%m%d-%H%M%S')}"

    return (
        "🔔 NDSP Trial Seat Alert\n\n"
        f"Event: {event_name}\n"
        f"Path: {path}\n"
        f"HTTP Status: {status_code}\n"
        f"Signal ID: {signal_id}\n\n"
        f"{_format_seats(seats)}\n\n"
        "تنبيه داخلي لإدارة مقاعد التجربة.\n"
        "ليس توصية مالية ولا إشارة تداول."
    )


class NDSPTrialTelegramAlertMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
    guard_response = await strict_email_phone_trial_guard(request)
    if guard_response is not None:
        return guard_response
    guard_response = await duplicate_activation_guard(request)
    if guard_response is not None:
        return guard_response
        response = await call_next(request)

        try:
            path = request.url.path
            method = request.method.upper()

            if method in ("POST", "PATCH", "PUT") and path in MONITORED_TRIAL_PATHS:
                if 200 <= int(response.status_code) < 300:
                    event_name = MONITORED_TRIAL_PATHS[path]
                    message = build_trial_alert_message(event_name, path, int(response.status_code))
                    send_telegram_message(message)
        except Exception as exc:
            print(f"[NDSP] trial telegram auto alert failed: {exc}")

        return response


@router.get("/api/trial/alerts/status")
def trial_alerts_status(request: Request) -> Dict[str, Any]:
    if not _is_admin_request(request):
        return {"ok": False, "error": "UNAUTHORIZED"}

    return {
        "ok": True,
        "configured": bool(_get_token() and _get_chat_ids()),
        "has_token": bool(_get_token()),
        "chat_ids_count": len(_get_chat_ids()),
        "monitored_paths": list(MONITORED_TRIAL_PATHS.keys()),
        "seats": _seats_snapshot(),
        "password_exposed": False,
        "token_exposed": False,
    }


@router.post("/api/trial/alerts/test")
async def trial_alerts_test(request: Request) -> Dict[str, Any]:
    if not _is_admin_request(request):
        return {"ok": False, "error": "UNAUTHORIZED"}

    payload: Dict[str, Any] = {}
    try:
        payload = await request.json()
        if not isinstance(payload, dict):
            payload = {}
    except Exception:
        payload = {}

    message = str(payload.get("message") or "").strip()
    if not message:
        message = build_trial_alert_message(
            "اختبار طبقة تنبيهات مقاعد التجربة",
            "/api/trial/alerts/test",
            200,
        )

    result = send_telegram_message(message)

    return {
        "ok": bool(result.get("ok")),
        "status": "sent" if result.get("ok") else "failed",
        "results": result.get("results", []),
        "token_exposed": False,
    }


@router.post("/api/trial/alerts/notify")
async def trial_alerts_notify(request: Request) -> Dict[str, Any]:
    if not _is_admin_request(request):
        return {"ok": False, "error": "UNAUTHORIZED"}

    payload: Dict[str, Any] = {}
    try:
        payload = await request.json()
        if not isinstance(payload, dict):
            payload = {}
    except Exception:
        payload = {}

    event_name = str(payload.get("event") or "تنبيه يدوي لمقاعد التجربة")
    path = str(payload.get("path") or "/api/trial/alerts/notify")

    message = build_trial_alert_message(event_name, path, 200)
    result = send_telegram_message(message)

    return {
        "ok": bool(result.get("ok")),
        "status": "sent" if result.get("ok") else "failed",
        "results": result.get("results", []),
        "token_exposed": False,
    }
