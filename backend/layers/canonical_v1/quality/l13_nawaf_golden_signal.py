from __future__ import annotations

from typing import Any, Mapping

from ..core.contracts import LayerResult
from .golden_signals import evaluate_golden_signals

LAYER_ID = "NDSP-CORE-L13"
CANONICAL_NAME = "nawaf_golden_signal"


def evaluate(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    signals = evaluate_golden_signals(
        asset_managers_overall=payload.get("asset_managers_overall"),
        asset_managers_weekly=payload.get("asset_managers_weekly"),
        leveraged_funds_weekly=payload.get("leveraged_funds_weekly"),
    )
    output = {
        "active": signals["golden_active"],
        "direction": signals["direction"],
        "rule": "AM_WEEKLY_EQUALS_LF_WEEKLY",
    }
    return LayerResult(
        LAYER_ID, CANONICAL_NAME,
        "ACTIVE" if output["active"] else "INACTIVE",
        95 if output["active"] else 0, output, blocking=False,
    ).to_dict()
