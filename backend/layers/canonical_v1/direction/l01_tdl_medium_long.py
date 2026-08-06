from __future__ import annotations

from typing import Any, Mapping

from ..core.contracts import LayerResult
from .investment_policy import evaluate_investment_policy

LAYER_ID = "NDSP-CORE-L01"
CANONICAL_NAME = "tdl_medium_long"


def evaluate(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    output = evaluate_investment_policy(
        asset_managers_overall=payload.get("asset_managers_overall"),
        asset_managers_weekly=payload.get("asset_managers_weekly"),
        leveraged_funds_weekly=payload.get("leveraged_funds_weekly"),
    )
    active = output["governing_direction"] in {"bullish", "bearish"}
    return LayerResult(
        LAYER_ID, CANONICAL_NAME,
        "ACTIVE" if active else "UNDER_REVIEW",
        90 if output["readiness_allowed"] else 65,
        output,
        blocking=not output["readiness_allowed"],
    ).to_dict()
