from __future__ import annotations
from math import isfinite
from typing import Any, Mapping, Sequence
from ..core.contracts import Direction, coerce_direction

def calculate_nmp(
    *, candles: Sequence[Mapping[str, Any]],
    indicator_values: Sequence[float | int | None],
    direction: Direction | str,
    indicator_name: str,
    timeframe: str | None = None,
) -> dict[str, Any]:
    resolved = coerce_direction(direction)
    if resolved not in {Direction.BULLISH, Direction.BEARISH}:
        return {
            "status": "PENDING_DIRECTION", "value": None,
            "direction": resolved.value, "indicator_name": indicator_name,
            "timeframe": timeframe, "price_source": "candle_open",
            "reason_code": "NMP_REQUIRES_DIRECTIONAL_CONTEXT",
        }
    if len(candles) != len(indicator_values):
        return {
            "status": "UNAVAILABLE", "value": None,
            "direction": resolved.value, "indicator_name": indicator_name,
            "timeframe": timeframe, "price_source": "candle_open",
            "reason_code": "NMP_CANDLE_INDICATOR_LENGTH_MISMATCH",
        }

    valid = []
    for index, (candle, raw) in enumerate(zip(candles, indicator_values)):
        try:
            value = float(raw)
            open_price = float(candle["open"])
        except (TypeError, ValueError, KeyError):
            continue
        if isfinite(value) and isfinite(open_price):
            valid.append((index, value, open_price))

    if not valid:
        return {
            "status": "UNAVAILABLE", "value": None,
            "direction": resolved.value, "indicator_name": indicator_name,
            "timeframe": timeframe, "price_source": "candle_open",
            "reason_code": "NMP_NO_VALID_INDICATOR_CANDLES",
        }

    if resolved == Direction.BULLISH:
        index, indicator_value, open_price = max(valid, key=lambda row: row[1])
        extreme_type = "highest"
    else:
        index, indicator_value, open_price = min(valid, key=lambda row: row[1])
        extreme_type = "lowest"

    return {
        "status": "AVAILABLE", "value": open_price,
        "direction": resolved.value, "indicator_name": indicator_name,
        "indicator_value": indicator_value, "extreme_type": extreme_type,
        "candle_index": index, "candle_open": open_price,
        "timeframe": timeframe, "price_source": "candle_open",
        "reason_code": None,
    }
