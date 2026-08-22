from __future__ import annotations

from typing import Any, Mapping

from ..core.contracts import LayerResult

LAYER_ID = "NDSP-CORE-L04"
CANONICAL_NAME = "correction_gate"


def evaluate(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    mode = payload.get("analysis_mode", "investment")
    if mode == "investment":
        allowed = bool((payload.get("l01") or {}).get("asset_managers_weekly_alignment"))
        role = "investment_weekly_correction_gate"
    else:
        allowed = bool((payload.get("l02") or {}).get("timing_eligible"))
        role = "speculative_timing_eligibility"
    output = {"mode": mode, "allowed": allowed, "role": role}
    return LayerResult(
        LAYER_ID, CANONICAL_NAME,
        "ALLOWED" if allowed else "MONITORING_ONLY",
        88 if allowed else 55, output, blocking=not allowed,
    ).to_dict()
