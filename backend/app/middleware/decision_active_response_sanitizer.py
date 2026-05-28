from __future__ import annotations

import json
import re
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


FORBIDDEN_KEY_TOKENS = {
    "tdl",
    "tdl_v2",
    "nmp",
    "cot",
    "tff",
    "timing_model",
    "timing_controller",
    "timing_authority",
    "decision_authority",
    "dominant_direction",
    "raw_score",
    "layer_score",
    "weights",
    "internal_bias",
    "governance_runtime",
    "governance_engine",
    "black_layer",
    "weekly_open_gravity",
    "golden_alignment",
    "raw_signal",
    "raw_intelligence",
    "institutional_mapping",
    "participant_mapping",
    "execution_logic",
    "authority_source",
    "risk_formula",
    "scoring_formula",
    "intelligence",
    "cot_mapping",
    "weekly_cot_mapping",
}

TERM_REPLACEMENTS = (
    ("Commitment of Traders", "Commitment Dataset"),
    ("TDL v2", "Directional Framework"),
    ("TDL", "Directional Framework"),
    ("NMP", "Structural Framework"),
    ("NMP-TDL", "Structural Framework"),
    ("Timing Authority", "Market State"),
    ("Decision Authority", "Decision State"),
    ("Timing Controller", "Market State"),
    ("Dominant Timed Direction", "Active Market Direction"),
    ("Black Layer", "Protective Risk Layer"),
    ("Decision Quality Stack", "Decision Quality Engine"),
    ("Governance Runtime", "Governance Engine"),
    ("Buy Signal", "Positive Bias"),
    ("Sell Signal", "Negative Bias"),
    ("Trade Execution", "User Controlled Action"),
    ("Automated Trading", "Analytical Automation"),
    ("Financial Advice", "Analytical Observation"),
    ("Take Profit", "Profit Objective"),
    ("Stop Loss", "Risk Protection"),
    ("timing_controller", "market_state"),
    ("TDL_ONLY", "Directional Framework"),
    ("Decision direction strictly follows the active timing_controller.", "Decision direction follows the active market state."),
    ("Final decision follows the active timing_controller when its direction is available.", "Final decision follows the active market state when available."),

)


def _normalize_key(key: Any) -> str:
    return str(key).strip().lower().replace("-", "_").replace(" ", "_")


def _is_forbidden_key(key: Any) -> bool:
    normalized = _normalize_key(key)
    return any(token in normalized for token in FORBIDDEN_KEY_TOKENS)


def _clean_text(value: str) -> str:
    result = value
    for src, dst in TERM_REPLACEMENTS:
        result = re.sub(
            rf"(?<![A-Za-z0-9_]){re.escape(src)}(?![A-Za-z0-9_])",
            dst,
            result,
            flags=re.IGNORECASE,
        )
    return result


def sanitize_decision_active_public_payload(payload: Any) -> Any:
    """
    Public response sanitizer only.
    Removes forbidden keys recursively and replaces sensitive terms in strings.
    Does not mutate runtime logic, direction, confidence, risk, or calculations.
    """
    def walk(obj: Any) -> Any:
        if isinstance(obj, dict):
            cleaned = {}
            for key, value in obj.items():
                if _is_forbidden_key(key):
                    continue
                cleaned[key] = walk(value)
            return cleaned

        if isinstance(obj, list):
            return [walk(item) for item in obj]

        if isinstance(obj, tuple):
            return [walk(item) for item in obj]

        if isinstance(obj, str):
            return _clean_text(obj)

        return obj

    return walk(payload)


class DecisionActiveResponseSanitizerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        path = request.url.path.rstrip("/") or "/"
        if path != "/decision":
            return response

        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type.lower():
            return response

        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        headers = dict(response.headers)
        headers.pop("content-length", None)

        if not body:
            return Response(
                content=body,
                status_code=response.status_code,
                headers=headers,
                media_type="application/json",
            )

        try:
            payload = json.loads(body.decode("utf-8"))
            safe_payload = sanitize_decision_active_public_payload(payload)
            safe_body = json.dumps(
                safe_payload,
                ensure_ascii=False,
                separators=(",", ":"),
            ).encode("utf-8")
        except Exception:
            safe_body = body

        return Response(
            content=safe_body,
            status_code=response.status_code,
            headers=headers,
            media_type="application/json",
        )


__all__ = [
    "DecisionActiveResponseSanitizerMiddleware",
    "sanitize_decision_active_public_payload",
]
