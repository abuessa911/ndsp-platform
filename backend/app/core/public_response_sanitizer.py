from __future__ import annotations

import copy
import json
import re
from typing import Any, Dict, Tuple

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


FORBIDDEN_PUBLIC_FIELDS = {
    "cot", "tff", "disaggregated", "legacy", "tdl", "tdl_v2", "nmp",
    "nmp_context", "timing_authority", "dominant_direction",
    "decision_authority", "timing_controller", "raw_score", "layer_score",
    "weights", "internal_bias", "governance_runtime", "governance_engine",
    "black_layer", "weekly_open_gravity", "golden_alignment", "raw_signal",
    "raw_intelligence", "institutional_mapping", "participant_mapping",
    "execution_logic", "authority_source", "risk_formula", "scoring_formula",
}

TERM_REPLACEMENTS: Tuple[Tuple[str, str], ...] = (
    ("Commitment of Traders", "Commitment Dataset"),
    ("TDL v2", "Directional Framework"),
    ("TDL", "Directional Framework"),
    ("NMP-TDL Quality", "Structural Quality Layer"),
    ("NMP-TDL", "Structural Framework"),
    ("NMP", "Structural Framework"),
    ("Timing Authority", "Market Timing State"),
    ("Decision Authority", "Market Decision State"),
    ("Dominant Timed Direction", "Active Market Direction"),
    ("Timing Controller", "Market Timing State"),
    ("Black Layer", "Protective Risk Layer"),
    ("Decision Quality Stack", "Decision Quality Engine"),
    ("Governance Runtime State Machine", "Governance Engine"),
    ("Asset Manager", "Long-Term Participants"),
    ("Leveraged Funds", "Short-Term Participants"),
    ("Dealer Intermediary", "Liquidity Participants"),
    ("Commercials", "Macro Participants"),
    ("Non-Commercials", "Speculative Participants"),
    ("Other Reportables", "Market Participants"),
    ("Managed Money", "Managed Participants"),
    ("Swap Dealers", "Liquidity Providers"),
    ("Trading Bot", "Analytical System"),
    ("Buy Signal", "Positive Market Bias"),
    ("Sell Signal", "Negative Market Bias"),
    ("Entry", "Decision Zone"),
    ("Take Profit", "Profit Objective"),
    ("Stop Loss", "Risk Protection"),
    ("Prediction", "Market Projection"),
    ("Guaranteed", "High Confidence"),
    ("Financial Advice", "Analytical Observation"),
    ("Trade Execution", "User Controlled Action"),
    ("Automated Trading", "Analytical Automation"),
    ("Smart Money", "Institutional Activity"),
    ("Alpha Engine", "Decision Engine"),
)

PUBLIC_PREFIXES = (
    "/decision",
    "/api/decision",
    "/api/v6/decision",
    "/alerts",
    "/api/v6/alerts",
    "/subscription/status",
    "/api/v6/subscription/status",
    "/status",
)

PROTECTED_PREFIXES = (
    "/admin",
    "/api/admin",
    "/internal",
    "/owner",
    "/debug",
    "/docs",
    "/redoc",
    "/openapi",
)


def _key_name(key: Any) -> str:
    return str(key).strip().lower().replace("-", "_")


def sanitize_text(value: str) -> str:
    out = value
    for src, dst in TERM_REPLACEMENTS:
        pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(src)}(?![A-Za-z0-9_])", re.IGNORECASE)
        out = pattern.sub(dst, out)
    return out


def sanitize_public_payload(payload: Any) -> Any:
    """
    Public response-layer sanitizer.
    Presentation only:
    - removes forbidden public fields
    - replaces sensitive words in string values
    - never mutates original payload
    - never recalculates direction/confidence/risk/decision state
    """
    data = copy.deepcopy(payload)

    def walk(obj: Any) -> Any:
        if isinstance(obj, dict):
            safe: Dict[Any, Any] = {}
            for key, value in obj.items():
                if _key_name(key) in FORBIDDEN_PUBLIC_FIELDS:
                    continue
                safe[key] = walk(value)
            return safe
        if isinstance(obj, list):
            return [walk(item) for item in obj]
        if isinstance(obj, str):
            return sanitize_text(obj)
        return obj

    return walk(data)


def public_payload_has_leak(payload: Any) -> bool:
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True).lower()
    for field in FORBIDDEN_PUBLIC_FIELDS:
        if f'"{field.lower()}"' in text:
            return True
    terms = [
        "commitment of traders", "tdl", "nmp", "timing authority",
        "decision authority", "black layer", "decision quality stack",
        "buy signal", "sell signal", "trade execution", "automated trading",
        "financial advice", "take profit", "stop loss",
    ]
    return any(term in text for term in terms)


def should_sanitize_path(path: str) -> bool:
    p = path.lower().rstrip("/") or "/"
    if any(p == item or p.startswith(item + "/") for item in PROTECTED_PREFIXES):
        return False
    return any(p == item or p.startswith(item + "/") for item in PUBLIC_PREFIXES)


class PublicResponseSanitizerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if not should_sanitize_path(request.url.path):
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
            raw_payload = json.loads(body.decode("utf-8"))
            safe_payload = sanitize_public_payload(raw_payload)
            safe_body = json.dumps(safe_payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        except Exception:
            safe_body = body

        return Response(
            content=safe_body,
            status_code=response.status_code,
            headers=headers,
            media_type="application/json",
        )
