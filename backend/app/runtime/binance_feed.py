from __future__ import annotations

from typing import Dict, Any, List
import urllib.request
import json


BINANCE_URL = "https://api.binance.com/api/v3/ticker/24hr"


def _state_from_percent(percent: float) -> str:
    if abs(percent) >= 3:
        return "VOLATILE"
    if percent > 0:
        return "ACTIVE"
    if percent < 0:
        return "CAUTION"
    return "NEUTRAL"


def get_binance_pulse(symbols: List[str]) -> List[Dict[str, Any]]:
    wanted = [s.upper() for s in symbols if s.upper().endswith("USDT")]

    if not wanted:
        return []

    with urllib.request.urlopen(BINANCE_URL, timeout=8) as response:
        raw = response.read().decode("utf-8")

    data = json.loads(raw)
    by_symbol = {str(x.get("symbol", "")).upper(): x for x in data}

    output = []

    for symbol in wanted:
        row = by_symbol.get(symbol)

        if not row:
            continue

        pct = float(row.get("priceChangePercent") or 0)
        price = float(row.get("lastPrice") or 0)

        output.append({
            "symbol": symbol,
            "last_price": round(price, 8),
            "change_percent": round(pct, 2),
            "state": _state_from_percent(pct),
            "source": "binance",
            "live": True,
        })

    return output
