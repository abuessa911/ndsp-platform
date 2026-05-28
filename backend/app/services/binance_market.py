from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any


BINANCE_API_BASE = "https://api.binance.com"
DEFAULT_INTERVAL = "1m"
DEFAULT_LIMIT = 120


def _symbol(symbol: str) -> str:
    return str(symbol or "").upper().replace("-", "").replace("/", "").strip()


def _num(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except Exception:
        return default


def _get_json(path: str, params: dict | None = None, timeout: int = 10):
    query = urllib.parse.urlencode(params or {})
    url = f"{BINANCE_API_BASE}{path}"
    if query:
        url = f"{url}?{query}"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "NDSP/1.0 market-data",
            "Accept": "application/json",
        },
    )

    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read().decode("utf-8")
        return json.loads(raw)


def _fetch_price(symbol: str) -> float | None:
    data = _get_json("/api/v3/ticker/price", {"symbol": symbol}, timeout=10)
    return _num(data.get("price"), default=0.0) or None


def _fetch_klines(symbol: str, interval: str = DEFAULT_INTERVAL, limit: int = DEFAULT_LIMIT) -> list[dict]:
    rows = _get_json(
        "/api/v3/klines",
        {
            "symbol": symbol,
            "interval": interval,
            "limit": int(limit),
        },
        timeout=12,
    )

    candles: list[dict] = []

    for row in rows or []:
        # Binance kline format:
        # [
        #   0 open time, 1 open, 2 high, 3 low, 4 close, 5 volume,
        #   6 close time, 7 quote volume, 8 trades, 9 taker buy base,
        #   10 taker buy quote, 11 ignore
        # ]
        try:
            candles.append(
                {
                    "time": int(row[0]),
                    "open": _num(row[1]),
                    "high": _num(row[2]),
                    "low": _num(row[3]),
                    "close": _num(row[4]),
                    "volume": _num(row[5]),
                    "close_time": int(row[6]),
                    "quote_volume": _num(row[7]),
                    "trades": int(row[8]),
                    "bid": _num(row[4]),
                    "ask": _num(row[4]),
                    "spread": 0.0,
                    "nmp_low": 0.0,
                    "nmp_high": 0.0,
                }
            )
        except Exception:
            continue

    return candles


def get_market_snapshot(symbol: str) -> dict:
    symbol_clean = _symbol(symbol)

    try:
        candles = _fetch_klines(symbol_clean)
        last = candles[-1] if candles else None
        price = (last or {}).get("close") or _fetch_price(symbol_clean)

        return {
            "symbol": symbol_clean,
            "symbol_id": f"{symbol_clean}-BINANCE",
            "price": price,
            "bid": (last or {}).get("bid"),
            "ask": (last or {}).get("ask"),
            "spread": (last or {}).get("spread", 0.0),
            "time": (last or {}).get("time"),
            "ohlcv": candles,
            "candles": candles,
            "last_candle": last,
            "source": "binance",
            "source_status": {
                "binance_available": bool(price),
                "interval": DEFAULT_INTERVAL,
                "candles": len(candles),
                "api": "binance_spot_rest",
            },
        }

    except Exception as exc:
        return {
            "symbol": symbol_clean,
            "symbol_id": f"{symbol_clean}-BINANCE",
            "price": None,
            "ohlcv": [],
            "candles": [],
            "last_candle": None,
            "source": "binance",
            "source_status": {
                "binance_available": False,
                "error": "binance_market_snapshot_failed",
                "detail": str(exc)[:180],
                "api": "binance_spot_rest",
            },
        }


def get_price(symbol: str) -> float:
    return float(get_market_snapshot(symbol).get("price") or 0.0)
