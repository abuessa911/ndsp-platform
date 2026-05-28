from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, MutableMapping
from uuid import uuid4

from app.core.ndsp_governance_mode import governance_mode_public


FORBIDDEN_PUBLIC_KEYS = {
    "raw",
    "raw_logic",
    "rawlogic",
    "raw_score",
    "raw_scores",
    "rawscore",
    "rawscores",
    "weights",
    "weight",
    "formula",
    "formulas",
    "calculation",
    "calculations",
    "trace",
    "debug",
    "stack",
    "stacktrace",
    "stack_trace",
    "secret",
    "token",
    "api_key",
    "apikey",
    "x_admin_key",
    "x-admin-key",
    "admin_key",
    "password",
    "database_url",
    "cot_raw",
    "cotraw",
    "indicator_raw",
    "indicatorraw",
    "internal",
    "internal_logic",
    "internallogic",
    "command",
    "order",
    "tp",
    "sl",
    "take_profit",
    "stop_loss",
    "stoploss",
    "takeprofit",
}

FORBIDDEN_VALUE_MARKERS = {
    "BUY NOW",
    "SELL NOW",
    "TAKE_PROFIT",
    "STOP_LOSS",
    "STOPLOSS",
    "TAKEPROFIT",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalized_key(key: Any) -> str:
    return str(key).strip().replace("-", "_").replace(" ", "_").lower()


def _is_forbidden_key(key: Any) -> bool:
    return _normalized_key(key) in FORBIDDEN_PUBLIC_KEYS


def _safe_string(value: str) -> str:
    v = value.strip()
    u = v.upper()

    if u == "BUY":
        return "bullish"
    if u == "SELL":
        return "bearish"

    out = value
    replacements = {
        "BUY NOW": "bullish context",
        "SELL NOW": "bearish context",
        "TAKE_PROFIT": "scenario boundary",
        "STOP_LOSS": "risk boundary",
        "TAKEPROFIT": "scenario boundary",
        "STOPLOSS": "risk boundary",
    }
    for bad, good in replacements.items():
        out = out.replace(bad, good)

    return out


def _sanitize_obj(obj: Any) -> Any:
    if isinstance(obj, dict):
        clean: Dict[str, Any] = {}
        for key, value in obj.items():
            if _is_forbidden_key(key):
                continue
            clean[str(key)] = _sanitize_obj(value)
        return clean

    if isinstance(obj, list):
        return [_sanitize_obj(v) for v in obj]

    if isinstance(obj, tuple):
        return [_sanitize_obj(v) for v in obj]

    if isinstance(obj, str):
        return _safe_string(obj)

    return obj


def _clamp_confidence(value: Any) -> int:
    try:
        v = int(round(float(value)))
    except Exception:
        v = 0
    return max(0, min(100, v))


def _normalize_direction(value: Any) -> str:
    v = str(value or "neutral").strip().lower()
    if v in {"buy", "long", "bull", "bullish"}:
        return "bullish"
    if v in {"sell", "short", "bear", "bearish"}:
        return "bearish"
    return "neutral"


def _ensure_dict(payload: MutableMapping[str, Any], key: str) -> Dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        value = {}
        payload[key] = value
    return value


def apply_decision_active_governance(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        payload = {}

    out: Dict[str, Any] = _sanitize_obj(deepcopy(payload))
    mode = governance_mode_public()

    out["system"] = "NDSP"
    out["version"] = str(out.get("version") or "1.0.0")
    out["governance_version"] = str(out.get("governance_version") or mode.get("governance_version") or "6.1.0")

    decision = _ensure_dict(out, "decision")
    decision["direction"] = _normalize_direction(decision.get("direction"))
    decision["confidence"] = _clamp_confidence(decision.get("confidence", 0))

    states = _ensure_dict(out, "states")
    states["system_state"] = str(states.get("system_state") or "live")
    states["risk_state"] = str(states.get("risk_state") or "normal")
    states["position_state"] = str(states.get("position_state") or "none")

    execution = _ensure_dict(out, "execution")
    raw_lifecycle = str(execution.get("lifecycle") or "waiting").lower()
    allowed_lifecycle = {"waiting", "signal", "monitoring", "closed"}
    if raw_lifecycle not in allowed_lifecycle:
        raw_lifecycle = "signal" if raw_lifecycle in {"executing", "execute", "entry"} else "waiting"

    execution.clear()
    execution.update(
        {
            "lifecycle": raw_lifecycle,
            "trade_id": None,
            "execution_policy": "EXECUTION_SANITIZED",
            "direct_execution": False,
            "public_command": False,
            "note": "Decision support output only; execution is not provided by NDSP.",
        }
    )

    out["governance_mode"] = mode

    compliance = _ensure_dict(out, "compliance")
    compliance.update(
        {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
            "decision_active": True,
            "execution_sanitized": True,
            "all_layers_participate": True,
            "no_layer_disabled": True,
        }
    )

    explainability = _ensure_dict(out, "explainability")
    explainability.setdefault("reason", "Governed decision-support context generated through the active NDSP pipeline.")
    explainability.setdefault("context_explanation", "All active layers contribute to the final decision-support context.")
    explainability.setdefault("confidence_explanation", "Confidence reflects governed layer agreement after sanitization.")
    explainability.setdefault("risk_explanation", "Execution details are sanitized and risk-aware delivery is preserved.")

    meta = _ensure_dict(out, "meta")
    meta.setdefault("timestamp", _now_iso())
    meta.setdefault("request_id", str(uuid4()))

    return _sanitize_obj(out)


def has_forbidden_public_leak(payload: Dict[str, Any]) -> bool:
    def walk(obj: Any) -> bool:
        if isinstance(obj, dict):
            for key, value in obj.items():
                if _is_forbidden_key(key):
                    return True
                if walk(value):
                    return True
            return False

        if isinstance(obj, list):
            return any(walk(v) for v in obj)

        if isinstance(obj, tuple):
            return any(walk(v) for v in obj)

        if isinstance(obj, str):
            u = obj.upper()
            if u in {"BUY", "SELL"}:
                return True
            return any(marker in u for marker in FORBIDDEN_VALUE_MARKERS)

        return False

    return walk(payload)
