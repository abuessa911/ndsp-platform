from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import requests
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from main import app as base_app

AUTH_SESSION_URL = os.getenv(
    "NDSP_AUTH_SESSION_URL",
    "http://127.0.0.1:19091/api/auth/session",
).strip()
DEFAULT_CAPABILITY_REGISTRY_PATH = Path(__file__).resolve().with_name("capability_registry.json")
CAPABILITY_REGISTRY_PATH = Path(
    os.getenv(
        "NDSP_CAPABILITY_REGISTRY_PATH",
        str(DEFAULT_CAPABILITY_REGISTRY_PATH),
    )
).resolve()
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


@base_app.get("/api/ui-bridge/analysis/capability-registry")
def capability_registry_summary():
    """Expose reconciliation proof only; never expose raw discovered record names/paths."""
    try:
        payload = json.loads(CAPABILITY_REGISTRY_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return JSONResponse(
            status_code=503,
            content={"ok": False, "error": "CAPABILITY_REGISTRY_UNAVAILABLE"},
        )

    if not isinstance(payload, dict) or payload.get("contract") != "NDSP_CAPABILITY_DISCOVERY_RECONCILIATION_V1":
        return JSONResponse(
            status_code=503,
            content={"ok": False, "error": "CAPABILITY_REGISTRY_INVALID"},
        )

    return {
        "ok": True,
        "contract": payload.get("contract"),
        "global_reconciled": payload.get("global_reconciled") is True,
        "record_count": int(payload.get("record_count") or 0),
        "expected_record_count": int(payload.get("expected_record_count") or 0),
        "silent_omission_count": int(payload.get("silent_omission_count") or 0),
        "parse_error_count": int(payload.get("parse_error_count") or 0),
        "governed_state_counts": payload.get("governed_state_counts") or {},
        "contract_status_counts": payload.get("contract_status_counts") or {},
        "runtime_capability_count_claimed": False,
        "activation_claim": False,
    }


app = base_app
