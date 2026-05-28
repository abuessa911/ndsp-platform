from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.public_response_sanitizer import sanitize_public_payload

router = APIRouter()


def _load_decision_runtime():
    """
    Lazy imports only inside request path to avoid app.main circular import at boot.
    """
    try:
        from app.core.ndsp_v4_pipeline import run_ndsp_v4_pipeline
        return "ndsp_v4_pipeline", run_ndsp_v4_pipeline
    except Exception:
        pass

    try:
        from app.core.decision_engine import run_decision
        return "decision_engine", run_decision
    except Exception:
        pass

    return "unavailable", None


@router.get("/public/decision")
async def public_decision_sanitized(symbol: str = "BTCUSDT") -> JSONResponse:
    """
    Public-safe decision endpoint.
    Response-layer sanitizer only.
    It does not patch the engine or mutate internal runtime values.
    """
    source, fn = _load_decision_runtime()

    if fn is None:
        raw_payload: Any = {
            "ok": False,
            "source": "public_decision_wrapper",
            "error": "decision_runtime_unavailable",
            "symbol": symbol,
        }
        return JSONResponse(content=sanitize_public_payload(raw_payload), status_code=503)

    try:
        try:
            raw_payload = fn(symbol=symbol)
        except TypeError:
            raw_payload = fn(symbol)

        if hasattr(raw_payload, "dict"):
            raw_payload = raw_payload.dict()
        elif hasattr(raw_payload, "model_dump"):
            raw_payload = raw_payload.model_dump()

        if not isinstance(raw_payload, dict):
            raw_payload = {
                "ok": True,
                "source": source,
                "symbol": symbol,
                "result": raw_payload,
            }
    except Exception as exc:
        raw_payload = {
            "ok": False,
            "source": source,
            "symbol": symbol,
            "error": f"decision_runtime_error:{type(exc).__name__}",
        }

    safe_payload = sanitize_public_payload(raw_payload)
    return JSONResponse(
        content=safe_payload,
        headers={"X-NDSP-Public-Sanitized": "true", "X-NDSP-Wrapper-Source": source},
    )
