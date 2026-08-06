from __future__ import annotations

from typing import Any, Mapping

from ..core.contracts import LayerResult
from ..quality.nmp_engine import calculate_nmp

LAYER_ID = "NDSP-CORE-L08"
CANONICAL_NAME = "nmp_confirmation"


def evaluate(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    output = calculate_nmp(
        candles=payload.get("candles") or [],
        indicator_values=payload.get("indicator_values") or [],
        direction=payload.get("direction") or (payload.get("l03") or {}).get("direction"),
        indicator_name=payload.get("indicator_name") or "UNKNOWN_INDICATOR",
        timeframe=payload.get("timeframe"),
    )
    available = output["status"] == "AVAILABLE"
    return LayerResult(
        LAYER_ID, CANONICAL_NAME, output["status"],
        90 if available else 0, output, blocking=not available,
    ).to_dict()
