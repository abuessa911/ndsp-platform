from __future__ import annotations

from typing import Any, Mapping

from ..core.contracts import LayerResult

LAYER_ID = "NDSP-CORE-L06"
CANONICAL_NAME = "temporal_day_logic"


def evaluate(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    mode = payload.get("analysis_mode", "investment")
    if mode == "investment":
        output = {
            "applicable": False,
            "changes_investment_direction": False,
            "role": "not_used_for_investment_direction",
        }
        return LayerResult(
            LAYER_ID, CANONICAL_NAME, "NOT_APPLICABLE",
            100, output, blocking=False,
        ).to_dict()
    timing_eligible = bool(payload.get("timing_eligible", False))
    output = {
        "applicable": True,
        "timing_eligible": timing_eligible,
        "role": "speculative_pre_tdl_eligibility",
    }
    return LayerResult(
        LAYER_ID, CANONICAL_NAME,
        "ELIGIBLE" if timing_eligible else "MONITORING_ONLY",
        90, output, blocking=not timing_eligible,
    ).to_dict()
