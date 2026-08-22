from __future__ import annotations
from ..core.contracts import coerce_direction, directional

def evaluate_speculative_policy(*, timing_eligible: bool, weekly_tdl_direction):
    tdl = coerce_direction(weekly_tdl_direction)
    return {
        "timing_eligible": bool(timing_eligible),
        "weekly_tdl_direction": tdl.value,
        "weekly_tdl_governing": True,
        "weekly_tdl_calculated_for_monitoring": True,
        "readiness_allowed": bool(timing_eligible and directional(tdl)),
        "state": (
            "READY"
            if timing_eligible and directional(tdl)
            else "MONITORING_ONLY"
            if directional(tdl)
            else "UNDER_REVIEW"
        ),
    }
