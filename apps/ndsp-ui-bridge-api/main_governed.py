from __future__ import annotations

import os
from typing import Any

import requests
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from main import app as base_app

AUTH_SESSION_URL = os.getenv(
    "NDSP_AUTH_SESSION_URL",
    "http://127.0.0.1:9020/api/auth/session",
).strip()
ANALYSIS_PREFIX = "/api/ui-bridge/analysis/"
AUTH_TIMEOUT_SECONDS = 5


def _validate_session(cookie_header: str) -> tuple[str, dict[str, Any] | None]:
    """Validate the canonical NDSP session without exposing or persisting cookies."""
    try:
        response = requests.get(
            AUTH_SESSION_URL,
            headers={
                "Accept": "application/json",
                "Cookie": cookie_header,
            },
            timeout=AUTH_TIMEOUT_SECONDS,
        )
    except requests.RequestException:
        return "UNAVAILABLE", None

    if response.status_code in {401, 403}:
        return "UNAUTHENTICATED", None
    if response.status_code != 200:
        return "UNAVAILABLE", None

    try:
        payload = response.json()
    except ValueError:
        return "UNAVAILABLE", None

    if not isinstance(payload, dict):
        return "UNAVAILABLE", None
    if payload.get("authenticated") is not True:
        return "UNAUTHENTICATED", None

    user = payload.get("user")
    if not isinstance(user, dict) or not user.get("id"):
        return "UNAUTHENTICATED", None

    return "AUTHENTICATED", user


@base_app.middleware("http")
async def governed_analysis_session_guard(request: Request, call_next):
    """Fail closed on governed analysis routes unless canonical session is valid."""
    if not request.url.path.startswith(ANALYSIS_PREFIX):
        return await call_next(request)

    cookie_header = request.headers.get("cookie", "").strip()
    if not cookie_header:
        return JSONResponse(
            status_code=401,
            content={"ok": False, "error": "AUTHENTICATION_REQUIRED"},
        )

    session_state, user = await run_in_threadpool(_validate_session, cookie_header)
    if session_state == "UNAVAILABLE":
        return JSONResponse(
            status_code=503,
            content={"ok": False, "error": "AUTH_SESSION_UNAVAILABLE"},
        )
    if session_state != "AUTHENTICATED" or user is None:
        return JSONResponse(
            status_code=401,
            content={"ok": False, "error": "AUTHENTICATION_REQUIRED"},
        )

    request.state.ndsp_user = {
        "id": str(user.get("id")),
        "role": str(user.get("role") or "USER"),
        "accountType": str(user.get("accountType") or "user"),
        "isAdmin": bool(user.get("isAdmin") is True),
    }
    return await call_next(request)


app = base_app
