from __future__ import annotations

from typing import Any, Mapping

from ..core.contracts import LayerResult
from .speculative_policy import evaluate_speculative_policy

LAYER_ID = "NDSP-CORE-L02"
CANONICAL_NAME = "tdl_short_speculative"


def evaluate(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    output = evaluate_speculative_policy(
        timing_eligible=bool(payload.get("timing_eligible", False)),
        weekly_tdl_direction=payload.get("weekly_tdl_direction"),
    )
    return LayerResult(
        LAYER_ID, CANONICAL_NAME, output["state"],
        90 if output["readiness_allowed"] else 60,
        output,
        blocking=not output["readiness_allowed"],
    ).to_dict()
