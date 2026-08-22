from __future__ import annotations
from ..core.contracts import coerce_direction, directional

def evaluate_investment_policy(
    *, asset_managers_overall, asset_managers_weekly, leveraged_funds_weekly
):
    overall = coerce_direction(asset_managers_overall)
    am_weekly = coerce_direction(asset_managers_weekly)
    lf_weekly = coerce_direction(leveraged_funds_weekly)

    weekly_aligned = directional(overall) and am_weekly == overall
    stability_aligned = directional(overall) and lf_weekly == overall

    return {
        "governing_direction": overall.value,
        "governing_source": "asset_managers_overall",
        "timing_rule_applied": False,
        "asset_managers_weekly_alignment": weekly_aligned,
        "correction_state": "ended" if weekly_aligned else "active",
        "leveraged_funds_weekly_alignment": stability_aligned,
        "correction_risk": "low" if stability_aligned else "elevated",
        "readiness_allowed": bool(directional(overall) and weekly_aligned),
    }
