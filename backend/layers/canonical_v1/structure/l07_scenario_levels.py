from __future__ import annotations

from typing import Any, Mapping

from ..core.contracts import LayerResult

LAYER_ID = "NDSP-CORE-L07"
CANONICAL_NAME = "scenario_levels"


def evaluate(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    levels = payload.get("scenario_levels")
    if not isinstance(levels, dict):
        output = {
            "status": "NOT_EVALUATED",
            "reason": "explicit_per_asset_per_timeframe_levels_required",
        }
        return LayerResult(
            LAYER_ID, CANONICAL_NAME, "NOT_EVALUATED",
            0, output, blocking=True,
        ).to_dict()
    required = {"activation", "arrival", "review", "invalidation"}
    missing = sorted(required - set(levels))
    status = "AVAILABLE" if not missing else "INCOMPLETE"
    output = {"status": status, "levels": levels, "missing": missing}
    return LayerResult(
        LAYER_ID, CANONICAL_NAME, status,
        90 if not missing else 40, output, blocking=bool(missing),
    ).to_dict()
