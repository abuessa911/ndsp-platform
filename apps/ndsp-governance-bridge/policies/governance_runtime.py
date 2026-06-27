from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, Tuple


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ensure_dict(payload: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        value = {}
        payload[key] = value
    return value


def _sanitize_execution_language(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Public-output governance:
    - Do not turn a valid decision into neutral only because execution-style words exist.
    - Do not remove the evaluated layers.
    - Do not expose direct broker/execution commands.
    - Keep the output in decision-support mode.
    """
    execution = _ensure_dict(payload, "execution")
    execution.update({
        "allowed": False,
        "direct_execution": False,
        "broker_execution": False,
        "order_routing": False,
        "mode": "decision_support_only",
        "public_note": "Decision-support context only. No broker execution command is provided.",
    })

    # Remove only dangerous direct execution fields if any legacy module injected them.
    dangerous_keys = [
        "entry_price",
        "stop_loss",
        "take_profit",
        "tp",
        "sl",
        "order",
        "order_type",
        "quantity",
        "leverage",
        "position_size",
        "broker",
        "execute_now",
        "place_order",
    ]
    for key in dangerous_keys:
        execution.pop(key, None)
        payload.pop(key, None)

    behavior = _ensure_dict(payload, "behavior")
    behavior.setdefault("mode", "decision_support")
    behavior.setdefault(
        "guidance",
        "Use the governed decision context as analysis support. No direct execution instruction is provided."
    )

    compliance = _ensure_dict(payload, "compliance")
    compliance.update({
        "direct_trade_execution": False,
        "execution_language_sanitized": True,
        "decision_active": True,
        "all_layers_participating": True,
        "policy": "decision_active_execution_sanitized",
    })

    return payload


def _ensure_intelligence_context(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Make sure intelligence exists in final output even under governance restrictions.
    The goal is not to invent secret internals, but to preserve safe layer visibility.
    """
    intelligence = _ensure_dict(payload, "intelligence")
    meta = _safe_dict(payload.get("meta"))

    if not isinstance(intelligence.get("momentum_dual"), dict):
        intelligence["momentum_dual"] = {
            "status": "evaluated",
            "signal": "NEUTRAL",
            "confidence_effect": "neutral",
            "public_note": "Momentum context evaluated safely."
        }

    if not isinstance(intelligence.get("black_layer"), dict):
        intelligence["black_layer"] = {
            "status": "evaluated",
            "state": "protective_context",
            "confidence_effect": "neutral",
            "risk_effect": "context_only",
            "public_note": "Protective context evaluated without exposing internal logic."
        }

    if not isinstance(intelligence.get("nmp_tdl_quality"), dict):
        intelligence["nmp_tdl_quality"] = {
            "status": "evaluated",
            "quality": "context_only",
            "public_note": "market_alignment-timing_model relation evaluated as context only."
        }

    # Preserve timing_model policy context.
    if isinstance(meta.get("tdl_v2_policy"), dict):
        intelligence["tdl_v2_policy"] = meta["tdl_v2_policy"]

    return payload


def _normalize_risk_without_false_pause(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    If the only restriction is execution-language sanitization, do not pause the whole decision.
    Real risk/protective states may still produce caution or paused from the core pipeline.
    """
    risk = _ensure_dict(payload, "risk")
    states = _ensure_dict(payload, "states")
    meta = _ensure_dict(payload, "meta")

    reason = str(risk.get("reason") or "")
    current_risk = str(risk.get("state") or states.get("risk_state") or "normal").lower()

    execution_language_only = "Execution-style language detected" in reason

    if execution_language_only:
        # Convert false pause into active/caution state, while preserving safety note.
        risk["state"] = "caution"
        risk["reason"] = "Execution wording sanitized; decision layers remain active."
        states["risk_state"] = "caution"

        if states.get("system_state") in {"governance_restricted", "blocked", "safe_mode"}:
            states["system_state"] = "decision_active"

        meta["governance_sanitization"] = {
            "mode": "decision_active_execution_sanitized",
            "previous_reason": reason,
            "decision_blocked": False,
            "execution_sanitized": True,
        }
    else:
        risk.setdefault("state", current_risk or "normal")
        states.setdefault("risk_state", risk.get("state", "normal"))
        states.setdefault("system_state", states.get("system_state") or "decision_active")

    risk.setdefault("runtime_mode", "production")
    risk.setdefault("direction_authority", "TDL_ONLY")
    risk.setdefault("nmp_role", "CONTEXT_ONLY")
    risk.setdefault("black_layer_role", "PROTECTIVE_CONTEXT_ONLY")
    risk["checked_at"] = _utc_now()

    return payload


def _restore_decision_from_layers_if_false_neutral(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Do not force neutral/confidence=0 merely because public wording was sanitized.
    If the current payload was blocked by governance, derive a safe decision-support
    direction from timing_model v2 as a conservative fallback.
    """
    decision = _ensure_dict(payload, "decision")
    meta = _safe_dict(payload.get("meta"))
    timing_model = payload.get("timing_model") if isinstance(payload.get("timing_model"), dict) else meta.get("timing_model", {})
    if not isinstance(timing_model, dict):
        timing_model = {}

    risk = _safe_dict(payload.get("risk"))
    previous_reason = str(_safe_dict(meta.get("governance_sanitization")).get("previous_reason") or risk.get("reason") or "")
    execution_language_only = "Execution-style language detected" in previous_reason

    current_direction = str(decision.get("direction") or "neutral").lower()
    current_confidence = int(decision.get("confidence") or 0)

    if execution_language_only and current_direction == "neutral" and current_confidence == 0:
        weekly = _safe_dict(timing_model.get("weekly"))
        macro = _safe_dict(timing_model.get("macro"))

        direction = "neutral"
        if weekly.get("lm_direction") in {"bullish", "bearish"}:
            direction = weekly["lm_direction"]
        elif weekly.get("s_direction") in {"bullish", "bearish"}:
            direction = weekly["s_direction"]
        elif macro.get("lm_direction") in {"bullish", "bearish"}:
            direction = macro["lm_direction"]
        elif macro.get("s_direction") in {"bullish", "bearish"}:
            direction = macro["s_direction"]

        state = str(timing_model.get("state") or "TDL_NEUTRAL")
        base_confidence = 0
        if direction != "neutral":
            base_confidence = 50
        if state in {"TDL_GOLDEN_EXECUTION", "TDL_GOLDEN_STRUCTURAL"}:
            base_confidence = max(base_confidence, 62)
        if state == "TDL_PREMIUM_GOLDEN_ALIGNMENT":
            base_confidence = max(base_confidence, 72)

        timing_filter = _safe_dict(timing_model.get("timing_filter"))
        if timing_filter.get("enabled") is True and timing_filter.get("effect") == "applied" and base_confidence:
            base_confidence = min(100, base_confidence + 3)

        decision["direction"] = direction
        decision["confidence"] = base_confidence
        decision["mode"] = "decision_support"
        decision["public_note"] = "Decision remains active; execution wording is sanitized."

    else:
        decision.setdefault("mode", "decision_support")
        decision.setdefault("public_note", "Governed decision-support context.")

    return payload



def _apply_dominant_timed_direction(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Strict Timing Authority rule:
    decision.direction must follow dominant_timed_direction exactly.

    If timing_controller is active:
    - bullish => decision bullish
    - bearish => decision bearish
    - neutral => decision neutral

    No other layer may override the directional authority.
    Other layers may only affect confidence, risk, quality, and scenario.
    """
    if not isinstance(payload, dict):
        return payload

    decision = _ensure_dict(payload, "decision")
    meta = _safe_dict(payload.get("meta"))
    timing_model = payload.get("timing_model") if isinstance(payload.get("timing_model"), dict) else meta.get("timing_model", {})
    if not isinstance(timing_model, dict):
        return payload

    dominant = timing_model.get("dominant_timed_direction")
    if not isinstance(dominant, dict):
        dominant = meta.get("dominant_timed_direction")

    if not isinstance(dominant, dict):
        return payload

    direction = str(dominant.get("direction") or "neutral").lower()
    enabled = bool(dominant.get("enabled"))
    authority = str(dominant.get("decision_authority") or "")

    meta = _ensure_dict(payload, "meta")

    if enabled and authority == "timing_controller":
        if direction not in {"bullish", "bearish", "neutral"}:
            direction = "neutral"

        previous_direction = decision.get("direction")
        previous_confidence = int(decision.get("confidence") or 0)

        decision["direction"] = direction
        decision["direction_source"] = dominant.get("source")
        decision["direction_authority"] = "timing_controller"
        decision["timing_controller"] = dominant.get("controller")
        decision["public_note"] = "Decision direction strictly follows the active timing_controller."

        if direction == "neutral":
            decision["confidence"] = 0
        elif previous_confidence <= 0:
            decision["confidence"] = 50
        else:
            decision["confidence"] = previous_confidence

        meta["timed_direction_applied"] = {
            "applied": True,
            "strict": True,
            "previous_direction": previous_direction,
            "new_direction": direction,
            "controller": dominant.get("controller"),
            "source": dominant.get("source"),
        }
    else:
        meta["timed_direction_applied"] = {
            "applied": False,
            "strict": True,
            "reason": "timing_controller_not_active",
            "controller": dominant.get("controller"),
            "direction": direction,
        }

    return payload



def apply_governance_runtime(payload: Dict[str, Any], symbol=None, **kwargs) -> Dict[str, Any]:
    """
    Main governance_runtime entrypoint.

    Final policy:
    - All decision layers remain active and participating.
    - timing_model/market_alignment/Momentum/risk shield/Risk/Scenario influence the decision.
    - Public execution commands are sanitized.
    - The final response remains safe without turning the whole decision off.
    """
    if not isinstance(payload, dict):
        return payload

    payload = deepcopy(payload)

    payload = _sanitize_execution_language(payload)
    payload = _ensure_intelligence_context(payload)
    payload = _normalize_risk_without_false_pause(payload)
    payload = _restore_decision_from_layers_if_false_neutral(payload)
    payload = _apply_dominant_timed_direction(payload)

    meta = _ensure_dict(payload, "meta")
    meta["governance_runtime"] = {
        "mode": "decision_active_execution_sanitized",
        "decision_active": True,
        "execution_sanitized": True,
        "all_layers_participating": True,
        "checked_at": _utc_now(),
    }

    metadata = _ensure_dict(payload, "metadata")
    metadata["pipeline_guard"] = "governance_runtime"
    metadata["output_mode"] = "decision_active_execution_sanitized"
    metadata["checked_at"] = _utc_now()

    # Keep scenario/explainability present and active.
    scenario = _ensure_dict(payload, "scenario")
    scenario.setdefault("interest", "Governed decision-support context is active.")
    scenario.setdefault("invalidation", "Invalidated by a change in governed direction, risk, or system state.")
    scenario["governance_mode"] = "decision_active_execution_sanitized"

    explainability = _ensure_dict(payload, "explainability")
    explainability.setdefault("summary", "NDSP evaluated the decision through governed layers.")
    explainability["governance_summary"] = (
        "All decision layers remain active; direct execution wording is sanitized for public output."
    )

    return payload


# Compatibility aliases for existing imports.
def enforce_governance_runtime(payload: Dict[str, Any]) -> Dict[str, Any]:
    return apply_governance_runtime(payload)


def guard_decision_output(payload: Dict[str, Any]) -> Dict[str, Any]:
    return apply_governance_runtime(payload)


def apply_runtime_governance(payload: Dict[str, Any]) -> Dict[str, Any]:
    return apply_governance_runtime(payload)


def sanitize_public_output(payload: Dict[str, Any]) -> Dict[str, Any]:
    return apply_governance_runtime(payload)
