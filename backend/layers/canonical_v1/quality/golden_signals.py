from __future__ import annotations
from ..core.contracts import coerce_direction, directional

def evaluate_golden_signals(
    *, asset_managers_overall, asset_managers_weekly, leveraged_funds_weekly
):
    am_overall = coerce_direction(asset_managers_overall)
    am_weekly = coerce_direction(asset_managers_weekly)
    lf_weekly = coerce_direction(leveraged_funds_weekly)

    golden = directional(am_weekly) and am_weekly == lf_weekly
    enhanced = golden and directional(am_overall) and am_overall == am_weekly
    direction = am_weekly.value if golden else "unknown"

    return {
        "golden_active": golden,
        "enhanced_active": enhanced,
        "direction": direction,
        "asset_managers_overall": am_overall.value,
        "asset_managers_weekly": am_weekly.value,
        "leveraged_funds_weekly": lf_weekly.value,
        "leveraged_funds_overall_used": False,
    }
