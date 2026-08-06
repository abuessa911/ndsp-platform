from __future__ import annotations

from typing import Any, Mapping

from ..core.contracts import LayerResult

LAYER_ID = "NDSP-CORE-L03"
CANONICAL_NAME = "market_direction_context"


def evaluate(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    mode = payload.get("analysis_mode", "investment")
    source = payload.get("l01", {}) if mode == "investment" else payload.get("l02", {})
    direction = source.get("governing_direction") or source.get("weekly_tdl_direction") or "unknown"
    output = {
        "analysis_mode": mode,
        "direction": direction,
        "source_layer": "L01" if mode == "investment" else "L02",
    }
    active = direction in {"bullish", "bearish"}
    return LayerResult(
        LAYER_ID, CANONICAL_NAME,
        "ACTIVE" if active else "UNDER_REVIEW",
        85, output, blocking=not active,
    ).to_dict()
