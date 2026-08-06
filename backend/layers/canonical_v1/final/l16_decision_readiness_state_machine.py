from __future__ import annotations

from typing import Any, Mapping

from ..core.contracts import DecisionReadinessState, LayerResult

LAYER_ID = "NDSP-CORE-L16"
CANONICAL_NAME = "decision_readiness_state_machine"


def evaluate(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    cot = payload.get("cot_validity") or {}
    if cot and not cot.get("decision_use_allowed", False):
        state = DecisionReadinessState.DATA_BLOCKED.value
        allowed = False
        reason = cot.get("reason_code") or "CFTC_DATA_NOT_CURRENT"
    elif bool((payload.get("l15") or {}).get("blocked")):
        state = DecisionReadinessState.BLOCKED_BY_DEVILS_ADVOCATE.value
        allowed = False
        reason = "DEVILS_ADVOCATE_FINAL_BLOCK"
    elif not bool((payload.get("l04") or {}).get("allowed")):
        state = DecisionReadinessState.MONITORING_ONLY.value
        allowed = False
        reason = "READINESS_GATE_NOT_ALLOWED"
    else:
        state = DecisionReadinessState.READY.value
        allowed = True
        reason = None
    output = {
        "single_truth_state": state,
        "allowed": allowed,
        "reason_code": reason,
    }
    return LayerResult(
        LAYER_ID, CANONICAL_NAME, state,
        100 if allowed else 60, output, blocking=not allowed,
    ).to_dict()
