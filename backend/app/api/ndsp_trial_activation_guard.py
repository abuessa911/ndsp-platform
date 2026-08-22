import json
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


_ACTIVE_WORDS = {"ACTIVE", "VERIFIED", "EMAIL_VERIFIED"}


def _pending_status(path: str, payload: Any) -> str:
    mode = ""
    if isinstance(payload, dict):
        mode = str(
            payload.get("mode")
            or payload.get("category")
            or payload.get("segment")
            or payload.get("user_type")
            or payload.get("registration_type")
            or ""
        ).lower()

    if "professional" in path.lower() or any(
        word in mode for word in ("professional", "specialist", "academic")
    ):
        return "PENDING_REVIEW"

    return "PENDING_EMAIL_VERIFICATION"


def _scrub_payload(obj: Any, pending: str) -> Any:
    if isinstance(obj, list):
        return [_scrub_payload(item, pending) for item in obj]

    if not isinstance(obj, dict):
        return obj

    cleaned = {}

    for key, value in obj.items():
        key_lower = str(key).lower()

        if key_lower in {
            "activation_token",
            "activationtoken",
            "verification_token",
            "verificationtoken",
            "email_verification_token",
            "emailverificationtoken",
        }:
            continue

        if key_lower in {
            "activation_url",
            "activationurl",
            "verification_url",
            "verificationurl",
            "email_verification_url",
            "emailverificationurl",
        }:
            continue

        if key_lower in {"status", "code"} and isinstance(value, str):
            if value.strip().upper() in _ACTIVE_WORDS:
                cleaned[key] = pending
                continue

        if key_lower in {
            "trial_started",
            "trial_active",
            "trialactive",
            "is_trial_active",
            "istrialactive",
        }:
            cleaned[key] = False
            continue

        if key_lower in {
            "trial_started_at",
            "trialstartedat",
            "trial_start_at",
            "trialstartat",
        }:
            cleaned[key] = None
            continue

        if isinstance(value, str) and "app.ndsp.app" in value:
            cleaned[key] = value.replace("https://app.ndsp.app", "https://my.ndsp.app").replace(
                "http://app.ndsp.app", "https://my.ndsp.app"
            )
            continue

        cleaned[key] = _scrub_payload(value, pending)

    cleaned["activation_required"] = True
    cleaned["trial_started"] = False
    cleaned["trial_started_at"] = None

    if pending == "PENDING_REVIEW":
        cleaned["admin_review_required"] = True
        cleaned["email_verification_required"] = True
        cleaned["message"] = "REGISTRATION_SUBMITTED_PENDING_REVIEW_TRIAL_NOT_STARTED"
    else:
        cleaned["email_verification_required"] = True
        cleaned["message"] = "REGISTRATION_SUBMITTED_CHECK_EMAIL_TRIAL_NOT_STARTED"

    return cleaned


class NDSPTrialActivationGuardMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        path = request.url.path

        if request.method.upper() != "POST":
            return response

        if not path.startswith("/api/trial/register"):
            return response

        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        if not body:
            return Response(
                content=body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        try:
            payload = json.loads(body.decode("utf-8"))
        except Exception:
            headers = dict(response.headers)
            headers.pop("content-length", None)
            headers.pop("content-encoding", None)
            headers.pop("transfer-encoding", None)
            return Response(
                content=body,
                status_code=response.status_code,
                headers=headers,
                media_type=response.media_type,
            )

        pending = _pending_status(path, payload)
        payload = _scrub_payload(payload, pending)

        new_body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

        headers = dict(response.headers)
        headers.pop("content-length", None)
        headers.pop("content-encoding", None)
        headers.pop("transfer-encoding", None)
        headers["x-ndsp-trial-activation-guard"] = "enabled"

        return Response(
            content=new_body,
            status_code=response.status_code,
            headers=headers,
            media_type="application/json",
        )
