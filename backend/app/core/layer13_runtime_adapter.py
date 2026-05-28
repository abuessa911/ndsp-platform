"""
NDSP Layer 13 Runtime Adapter

Purpose:
- Enrich runtime decision contracts with quality fields only.

Allowed:
- confidence
- grade
- quality_label
- layer13_bound flag

Forbidden:
- direction mutation
- timing_controller mutation
- risk_state mutation
- execution_allowed mutation
- execution_mode mutation
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Mapping

from app.core.decision_quality_stack import compute_decision_quality


PROTECTED_FIELDS = (
    "direction",
    "timing_controller",
    "risk_state",
    "decision_state",
    "execution_allowed",
    "execution_mode",
)


def _as_dict(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return deepcopy(payload)
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    if hasattr(payload, "dict"):
        return payload.dict()
    return {"value": payload}


def _get_decision_container(contract: Dict[str, Any]) -> Dict[str, Any]:
    decision = contract.get("decision")
    if isinstance(decision, dict):
        return decision
    return _ndsp_ensure_decision_risk_state(contract)


def _extract_base_confidence(decision: Mapping[str, Any], default: float = 50.0) -> float:
    for key in ("confidence", "confidence_score", "final_confidence", "quality_score"):
        value = decision.get(key)
        if isinstance(value, (int, float)):
            return float(value)
    return default


def _extract_effects(contract: Mapping[str, Any], decision: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Extract internal quality effects defensively.

    This adapter accepts multiple possible field names without requiring the
    runtime to expose sensitive names publicly.
    """
    intelligence = contract.get("intelligence", {})
    if not isinstance(intelligence, dict):
        intelligence = {}

    quality_context = contract.get("quality_context", {})
    if not isinstance(quality_context, dict):
        quality_context = {}

    risk = contract.get("risk", {})
    if not isinstance(risk, dict):
        risk = {}

    effects = {
        "golden_alignment_active": bool(
            contract.get("golden_alignment_active")
            or quality_context.get("golden_alignment_active")
            or intelligence.get("golden_alignment_active")
        ),
        "above_weekly_open": bool(
            contract.get("above_weekly_open")
            or quality_context.get("above_weekly_open")
            or intelligence.get("above_weekly_open")
            or intelligence.get("weekly_open_support")
        ),
        "weekly_open_support": bool(
            contract.get("weekly_open_support")
            or quality_context.get("weekly_open_support")
            or intelligence.get("weekly_open_support")
        ),
        "momentum_aligned": bool(
            contract.get("momentum_aligned")
            or quality_context.get("momentum_aligned")
            or intelligence.get("momentum_aligned")
        ),
        "macro_aligned": bool(
            contract.get("macro_aligned")
            or quality_context.get("macro_aligned")
            or intelligence.get("macro_aligned")
        ),
        "participant_conflict": bool(
            contract.get("participant_conflict")
            or quality_context.get("participant_conflict")
            or intelligence.get("participant_conflict")
        ),
        "correction_state": bool(
            contract.get("correction_state")
            or quality_context.get("correction_state")
            or intelligence.get("correction_state")
        ),
        "data_degraded": bool(
            contract.get("data_degraded")
            or quality_context.get("data_degraded")
            or decision.get("data_degraded")
        ),
        "session_degraded": bool(
            contract.get("session_degraded")
            or quality_context.get("session_degraded")
            or decision.get("session_degraded")
        ),
        "protective_risk": bool(
            contract.get("protective_risk")
            or risk.get("protective_risk")
            or str(decision.get("risk_state", "")).lower() in {"caution", "blocked", "restricted"}
        ),
        "black_layer_danger": bool(
            contract.get("black_layer_danger")
            or risk.get("black_layer_danger")
            or str(decision.get("decision_state", "")).lower() in {"blocked", "protective_block"}
        ),
    }

    return effects


def enrich_decision_contract_with_layer13(contract_payload: Any, public: bool = True) -> Dict[str, Any]:
    """
    Return a new enriched contract.

    Adds quality fields only and preserves protected fields unchanged.
    """
    contract = _as_dict(contract_payload)
    decision = _get_decision_container(contract)

    before = {k: decision.get(k) for k in PROTECTED_FIELDS if k in decision}

    base_conf = _extract_base_confidence(decision)
    effects = _extract_effects(contract, decision)
    quality = compute_decision_quality(base_conf, effects, public=public)

    # Only quality fields are added/updated.
    if "decision" in contract and isinstance(contract["decision"], dict):
        target = contract["decision"]
    else:
        target = contract

    target["confidence"] = quality.get("final_confidence")
    target["grade"] = quality.get("grade")
    target["quality_label"] = quality.get("quality_label")
    target["layer13_bound"] = True

    after = {k: target.get(k) for k in PROTECTED_FIELDS if k in target}

    if before != after:
        raise RuntimeError(
            "Layer13 adapter attempted protected field mutation: "
            f"before={before} after={after}"
        )

    return _ndsp_ensure_decision_risk_state(contract)

# NDSP runtime safety fallback: public decision must always carry risk_state.

def _ndsp_ensure_decision_risk_state(contract):
    try:
        if isinstance(contract, dict):
            decision = contract.setdefault("decision", {})
            if isinstance(decision, dict):
                if not decision.get("risk_state"):
                    risk_state = None
                    risk = contract.get("risk")
                    governance = contract.get("governance")
                    if isinstance(risk, dict):
                        risk_state = risk.get("risk_state") or risk.get("state")
                    if isinstance(governance, dict):
                        risk_state = risk_state or governance.get("risk_state")
                    decision["risk_state"] = str(risk_state or "normal").lower()

                decision["execution_allowed"] = False
                decision["execution_mode"] = "decision_support_only"

            governance = contract.setdefault("governance", {})
            if isinstance(governance, dict):
                governance["decision_support_only"] = True
                governance["direct_execution"] = False
                governance["execution_allowed"] = False
                governance["execution_mode"] = "decision_support_only"
    except Exception:
        pass
    return contract
