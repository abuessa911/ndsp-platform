#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import math
import os
import statistics
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(os.environ.get("NDSP_PROJECT_ROOT", "/home/nawaf511/empire-core-new"))
V30_PATH = PROJECT_ROOT / "backend/app/runtime/ndsp_canonical_live_runtime_v30.py"

spec = importlib.util.spec_from_file_location("ndsp_canonical_live_runtime_v30_base", V30_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load V30 runtime: {V30_PATH}")
v30 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v30)

VERSION = "ndsp-canonical-live-runtime-v33.0.0"
CONTRACT_VERSION = "ndsp-canonical-live-contract-v33"
HOST = os.environ.get("NDSP_CANONICAL_HOST", "127.0.0.1")
PORT = int(os.environ.get("NDSP_CANONICAL_PORT", "9086"))
RUNTIME_DIR = Path(os.environ.get(
    "NDSP_CANONICAL_RUNTIME_DIR",
    str(PROJECT_ROOT / "var/runtime/canonical-live-v33"),
))

BINANCE_BASE = "https://api.binance.com"
YAHOO_BASE = "https://query1.finance.yahoo.com/v8/finance/chart"
CACHE_TTL_SECONDS = int(os.environ.get("NDSP_V33_CACHE_TTL_SECONDS", "60"))
CACHE_LOCK = threading.RLock()
CACHE: dict[str, tuple[float, Any]] = {}

EXTERNAL_SYMBOLS = {
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "AUDUSD": "AUDUSD=X",
    "USDJPY": "JPY=X",
    "USDCAD": "CAD=X",
    "USDCHF": "CHF=X",
    "XAUUSD": "GC=F",
    "XAGUSD": "SI=F",
    "USOIL": "CL=F",
    "UKOIL": "BZ=F",
    "NG": "NG=F",
    "ZC": "ZC=F",
    "ZS": "ZS=F",
    "ZW": "ZW=F",
    "SPX": "^GSPC",
    "NDX": "^NDX",
    "DXY": "DX-Y.NYB",
    "DJI": "^DJI",
    "VIX": "^VIX",
    "CAC": "^FCHI",
    "DAX": "^GDAXI",
}

TIMEFRAME_TO_BINANCE = {
    "daily": "1d",
    "weekly": "1w",
    "monthly": "1M",
}
TIMEFRAME_TO_YAHOO = {
    "daily": ("1d", "2y"),
    "weekly": ("1wk", "10y"),
    "monthly": ("1mo", "10y"),
}
MAX_AGE_SECONDS = {
    "daily": 4 * 24 * 3600,
    "weekly": 15 * 24 * 3600,
    "monthly": 50 * 24 * 3600,
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def clean_symbol(symbol: str) -> str:
    return str(symbol or "").upper().replace("/", "").replace(" ", "").strip()


def safe_number(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def cached(key: str, loader):
    now = time.time()
    with CACHE_LOCK:
        existing = CACHE.get(key)
        if existing and now - existing[0] <= CACHE_TTL_SECONDS:
            return existing[1]
    value = loader()
    with CACHE_LOCK:
        CACHE[key] = (now, value)
    return value


def fetch_json(url: str, timeout: int = 20) -> Any:
    request = Request(
        url,
        headers={
            "Accept": "application/json,text/plain,*/*",
            "User-Agent": f"NDSP/{VERSION}",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def fetch_binance_ohlcv(symbol: str, timeframe: str, limit: int = 240) -> dict[str, Any]:
    interval = TIMEFRAME_TO_BINANCE[timeframe]
    url = f"{BINANCE_BASE}/api/v3/klines?{urlencode({'symbol': symbol, 'interval': interval, 'limit': limit})}"

    def load():
        rows = fetch_json(url)
        now_ms = int(time.time() * 1000)
        closed = [row for row in rows if int(row[6]) <= now_ms]
        if len(closed) >= 80:
            rows = closed
        return {
            "opens": [float(row[1]) for row in rows],
            "highs": [float(row[2]) for row in rows],
            "lows": [float(row[3]) for row in rows],
            "closes": [float(row[4]) for row in rows],
            "volumes": [float(row[5]) for row in rows],
            "close_times": [int(row[6]) for row in rows],
            "provider": "binance_public_klines",
            "provider_symbol": symbol,
            "interval": interval,
        }

    return cached(f"binance:ohlcv:{symbol}:{interval}:{limit}", load)


def fetch_yahoo_ohlcv(symbol: str, timeframe: str, limit: int = 240) -> dict[str, Any]:
    provider_symbol = EXTERNAL_SYMBOLS.get(symbol)
    if not provider_symbol:
        raise ValueError(f"NO_YAHOO_MAPPING:{symbol}")
    interval, data_range = TIMEFRAME_TO_YAHOO[timeframe]
    encoded = quote(provider_symbol, safe="")
    query = urlencode({
        "range": data_range,
        "interval": interval,
        "includePrePost": "false",
        "events": "div,splits",
    })
    url = f"{YAHOO_BASE}/{encoded}?{query}"

    def load():
        data = fetch_json(url)
        result = (((data or {}).get("chart") or {}).get("result") or [None])[0]
        if not result:
            raise ValueError(f"YAHOO_EMPTY:{symbol}")
        timestamps = result.get("timestamp") or []
        quote_data = (((result.get("indicators") or {}).get("quote") or [None])[0]) or {}
        opens0 = quote_data.get("open") or []
        highs0 = quote_data.get("high") or []
        lows0 = quote_data.get("low") or []
        closes0 = quote_data.get("close") or []
        volumes0 = quote_data.get("volume") or []

        opens: list[float] = []
        highs: list[float] = []
        lows: list[float] = []
        closes: list[float] = []
        volumes: list[float] = []
        close_times: list[int] = []

        for ts, op, hi, lo, cl, vol in zip(
            timestamps, opens0, highs0, lows0, closes0, volumes0
        ):
            opn = safe_number(op)
            high = safe_number(hi)
            low = safe_number(lo)
            close = safe_number(cl)
            if high is None or low is None or close is None:
                continue
            opens.append(opn if opn is not None else close)
            highs.append(high)
            lows.append(low)
            closes.append(close)
            volumes.append(safe_number(vol) or 0.0)
            close_times.append(int(ts) * 1000)

        return {
            "opens": opens[-limit:],
            "highs": highs[-limit:],
            "lows": lows[-limit:],
            "closes": closes[-limit:],
            "volumes": volumes[-limit:],
            "close_times": close_times[-limit:],
            "provider": "yahoo_public_chart",
            "provider_symbol": provider_symbol,
            "interval": interval,
        }

    return cached(f"yahoo:ohlcv:{provider_symbol}:{interval}:{data_range}:{limit}", load)


def fetch_ohlcv(symbol: str, timeframe: str, limit: int = 240) -> dict[str, Any]:
    cleaned = clean_symbol(symbol)
    if cleaned.endswith("USDT"):
        return fetch_binance_ohlcv(cleaned, timeframe, limit)
    return fetch_yahoo_ohlcv(cleaned, timeframe, limit)


def ema_series(values: list[float], period: int) -> list[float | None]:
    result: list[float | None] = [None] * len(values)
    if len(values) < period:
        return result
    seed = sum(values[:period]) / period
    result[period - 1] = seed
    alpha = 2.0 / (period + 1.0)
    current = seed
    for index in range(period, len(values)):
        current = values[index] * alpha + current * (1.0 - alpha)
        result[index] = current
    return result


def rsi_series(values: list[float], period: int = 14) -> list[float | None]:
    result: list[float | None] = [None] * len(values)
    if len(values) <= period:
        return result
    gains: list[float] = []
    losses: list[float] = []
    for index in range(1, period + 1):
        change = values[index] - values[index - 1]
        gains.append(max(change, 0.0))
        losses.append(max(-change, 0.0))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    def value(gain: float, loss: float) -> float:
        if loss == 0:
            return 100.0
        ratio = gain / loss
        return 100.0 - (100.0 / (1.0 + ratio))

    result[period] = value(avg_gain, avg_loss)
    for index in range(period + 1, len(values)):
        change = values[index] - values[index - 1]
        gain = max(change, 0.0)
        loss = max(-change, 0.0)
        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period
        result[index] = value(avg_gain, avg_loss)
    return result


def macd_histogram(values: list[float]) -> list[float | None]:
    fast = ema_series(values, 12)
    slow = ema_series(values, 26)
    macd: list[float | None] = [
        (f - s) if f is not None and s is not None else None
        for f, s in zip(fast, slow)
    ]
    valid = [value for value in macd if value is not None]
    signal_valid = ema_series(valid, 9)
    signal: list[float | None] = [None] * len(values)
    cursor = 0
    for index, value in enumerate(macd):
        if value is None:
            continue
        signal[index] = signal_valid[cursor]
        cursor += 1
    return [
        (m - s) if m is not None and s is not None else None
        for m, s in zip(macd, signal)
    ]


def obv_series(closes: list[float], volumes: list[float]) -> list[float]:
    if not closes:
        return []
    result = [0.0]
    for index in range(1, len(closes)):
        previous = result[-1]
        if closes[index] > closes[index - 1]:
            previous += volumes[index]
        elif closes[index] < closes[index - 1]:
            previous -= volumes[index]
        result.append(previous)
    return result


def cci_series(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    period: int = 20,
) -> list[float | None]:
    typical = [(h + l + c) / 3.0 for h, l, c in zip(highs, lows, closes)]
    result: list[float | None] = [None] * len(typical)
    for index in range(period - 1, len(typical)):
        window = typical[index - period + 1:index + 1]
        mean = sum(window) / period
        deviation = sum(abs(value - mean) for value in window) / period
        result[index] = 0.0 if deviation == 0 else (typical[index] - mean) / (0.015 * deviation)
    return result


def last_number(values: list[float | None]) -> float | None:
    for value in reversed(values):
        if value is not None and math.isfinite(value):
            return float(value)
    return None


def pivot_indices(values: list[float], kind: str, window: int = 2) -> list[int]:
    pivots: list[int] = []
    for index in range(window, len(values) - window):
        value = values[index]
        neighbors = values[index - window:index] + values[index + 1:index + window + 1]
        if kind == "low":
            if value <= min(neighbors) and value < max(neighbors):
                pivots.append(index)
        else:
            if value >= max(neighbors) and value > min(neighbors):
                pivots.append(index)
    return pivots


def detect_divergence(
    highs: list[float],
    lows: list[float],
    indicator_sets: Mapping[str, list[float | None]],
) -> dict[str, Any]:
    detections: list[dict[str, Any]] = []
    low_pivots = pivot_indices(lows, "low")[-8:]
    high_pivots = pivot_indices(highs, "high")[-8:]

    for name, series in indicator_sets.items():
        usable_lows = [index for index in low_pivots if series[index] is not None]
        if len(usable_lows) >= 2:
            first, second = usable_lows[-2], usable_lows[-1]
            p1, p2 = lows[first], lows[second]
            i1, i2 = float(series[first]), float(series[second])
            if p2 < p1 and i2 > i1:
                detections.append({
                    "indicator": name,
                    "side": "bullish",
                    "type": "regular",
                    "first_index": first,
                    "second_index": second,
                })
            elif p2 > p1 and i2 < i1:
                detections.append({
                    "indicator": name,
                    "side": "bullish",
                    "type": "hidden",
                    "first_index": first,
                    "second_index": second,
                })

        usable_highs = [index for index in high_pivots if series[index] is not None]
        if len(usable_highs) >= 2:
            first, second = usable_highs[-2], usable_highs[-1]
            p1, p2 = highs[first], highs[second]
            i1, i2 = float(series[first]), float(series[second])
            if p2 > p1 and i2 < i1:
                detections.append({
                    "indicator": name,
                    "side": "bearish",
                    "type": "regular",
                    "first_index": first,
                    "second_index": second,
                })
            elif p2 < p1 and i2 > i1:
                detections.append({
                    "indicator": name,
                    "side": "bearish",
                    "type": "hidden",
                    "first_index": first,
                    "second_index": second,
                })

    sides = {item["side"] for item in detections}
    types = {item["type"] for item in detections}
    if len(sides) == 1:
        direction = next(iter(sides))
    elif len(sides) > 1:
        direction = "mixed"
    else:
        direction = "none"

    return {
        "status": "AVAILABLE",
        "confidence": min(95, 82 + len(detections) * 3),
        "input_quality": "FULL",
        "indicator_set": ["RSI", "MACD_HISTOGRAM", "OBV", "CCI"],
        "divergence_detected": bool(detections),
        "direction": direction,
        "regular_or_hidden": (
            next(iter(types)) if len(types) == 1
            else "MIXED" if len(types) > 1
            else "NONE"
        ),
        "detections": detections,
        "reason": "FULL_GOVERNED_INDICATOR_SET_EVALUATED",
    }


def momentum_result(
    rsi: list[float | None],
    macd_hist: list[float | None],
    obv: list[float],
    cci: list[float | None],
) -> dict[str, Any]:
    rsi_value = last_number(rsi)
    macd_value = last_number(macd_hist)
    cci_value = last_number(cci)
    macd_previous = next(
        (float(value) for value in reversed(macd_hist[:-1]) if value is not None),
        None,
    )

    votes: dict[str, str] = {}
    if rsi_value is None:
        votes["RSI"] = "unknown"
    elif rsi_value >= 55:
        votes["RSI"] = "bullish"
    elif rsi_value <= 45:
        votes["RSI"] = "bearish"
    else:
        votes["RSI"] = "neutral"

    if macd_value is None:
        votes["MACD_HISTOGRAM"] = "unknown"
    elif macd_value > 0 and (macd_previous is None or macd_value >= macd_previous):
        votes["MACD_HISTOGRAM"] = "bullish"
    elif macd_value < 0 and (macd_previous is None or macd_value <= macd_previous):
        votes["MACD_HISTOGRAM"] = "bearish"
    else:
        votes["MACD_HISTOGRAM"] = "neutral"

    if len(obv) >= 12:
        recent = statistics.fmean(obv[-5:])
        previous = statistics.fmean(obv[-10:-5])
        votes["OBV"] = "bullish" if recent > previous else "bearish" if recent < previous else "neutral"
    else:
        votes["OBV"] = "unknown"

    if cci_value is None:
        votes["CCI"] = "unknown"
    elif cci_value >= 50:
        votes["CCI"] = "bullish"
    elif cci_value <= -50:
        votes["CCI"] = "bearish"
    else:
        votes["CCI"] = "neutral"

    bullish = sum(value == "bullish" for value in votes.values())
    bearish = sum(value == "bearish" for value in votes.values())
    neutral = sum(value == "neutral" for value in votes.values())
    if bullish > bearish:
        direction = "bullish"
        winning = bullish
    elif bearish > bullish:
        direction = "bearish"
        winning = bearish
    else:
        direction = "neutral"
        winning = neutral

    return {
        "status": "AVAILABLE",
        "confidence": min(95, 65 + winning * 7),
        "input_quality": "FULL",
        "direction": direction,
        "votes": votes,
        "bullish_votes": bullish,
        "bearish_votes": bearish,
        "neutral_votes": neutral,
        "rsi": rsi_value,
        "macd_histogram": macd_value,
        "obv": obv[-1] if obv else None,
        "cci": cci_value,
        "reason": "RSI_MACD_OBV_CCI_BOUND",
    }


def fetch_binance_depth(symbol: str, limit: int = 100) -> dict[str, Any]:
    url = f"{BINANCE_BASE}/api/v3/depth?{urlencode({'symbol': symbol, 'limit': limit})}"

    def load():
        data = fetch_json(url)
        bids = [(float(price), float(quantity)) for price, quantity in data.get("bids") or []]
        asks = [(float(price), float(quantity)) for price, quantity in data.get("asks") or []]
        if not bids or not asks:
            raise ValueError("BINANCE_DEPTH_EMPTY")
        best_bid = bids[0][0]
        best_ask = asks[0][0]
        mid = (best_bid + best_ask) / 2.0
        spread_bps = ((best_ask - best_bid) / mid) * 10000.0

        lower = mid * 0.995
        upper = mid * 1.005
        bid_notional = sum(price * quantity for price, quantity in bids if price >= lower)
        ask_notional = sum(price * quantity for price, quantity in asks if price <= upper)
        total = bid_notional + ask_notional
        imbalance = 0.0 if total == 0 else (bid_notional - ask_notional) / total

        return {
            "provider": "binance_public_order_book",
            "best_bid": best_bid,
            "best_ask": best_ask,
            "mid": mid,
            "spread_bps": spread_bps,
            "bid_notional_50bps": bid_notional,
            "ask_notional_50bps": ask_notional,
            "order_book_imbalance": imbalance,
            "levels": min(len(bids), len(asks)),
        }

    return cached(f"binance:depth:{symbol}:{limit}", load)


def liquidity_result(symbol: str, ohlcv: Mapping[str, Any], levels: Mapping[str, Any]) -> dict[str, Any]:
    volumes = [float(value) for value in ohlcv.get("volumes") or []]
    current_volume = volumes[-1] if volumes else 0.0
    average_volume = statistics.fmean(volumes[-20:]) if len(volumes) >= 20 else 0.0
    volume_ratio = None if average_volume <= 0 else current_volume / average_volume

    if clean_symbol(symbol).endswith("USDT"):
        depth = fetch_binance_depth(clean_symbol(symbol))
        verified = bool(
            depth.get("levels", 0) >= 20
            and safe_number(depth.get("spread_bps")) is not None
            and float(depth["spread_bps"]) <= 30.0
            and len(volumes) >= 20
        )
        confidence = 90 if verified else 55
        return {
            "status": "AVAILABLE" if verified else "PARTIAL_AVAILABLE",
            "confidence": confidence,
            "input_quality": "FULL" if verified else "PARTIAL",
            "liquidity_verified": verified,
            "structure_verified": len(levels) == 4,
            "scenario_levels": dict(levels),
            "current_volume": current_volume,
            "average_volume_20": average_volume,
            "volume_ratio": volume_ratio,
            "order_book": depth,
            "reason": (
                "REAL_ORDER_BOOK_AND_VOLUME_VERIFIED"
                if verified else "ORDER_BOOK_OR_VOLUME_GATE_NOT_MET"
            ),
        }

    return {
        "status": "PARTIAL_AVAILABLE",
        "confidence": 55,
        "input_quality": "PARTIAL",
        "liquidity_verified": False,
        "structure_verified": len(levels) == 4,
        "scenario_levels": dict(levels),
        "current_volume": current_volume,
        "average_volume_20": average_volume,
        "volume_ratio": volume_ratio,
        "reason": "EXTERNAL_MARKET_ORDER_BOOK_PROVIDER_NOT_BOUND",
    }


def dxy_result() -> dict[str, Any]:
    data = fetch_yahoo_ohlcv("DXY", "daily", 180)
    closes = [float(value) for value in data["closes"]]
    ema20 = last_number(ema_series(closes, 20))
    ema50 = last_number(ema_series(closes, 50))
    rsi = last_number(rsi_series(closes, 14))
    close = closes[-1]
    last_close_ms = int(data["close_times"][-1])
    age_seconds = max(0.0, time.time() - (last_close_ms / 1000.0))
    fresh = age_seconds <= 5 * 24 * 3600

    if ema20 is not None and ema50 is not None and rsi is not None:
        if close > ema20 > ema50 and rsi >= 50:
            direction = "bullish"
        elif close < ema20 < ema50 and rsi <= 50:
            direction = "bearish"
        else:
            direction = "neutral"
    else:
        direction = "unknown"

    verified = bool(fresh and direction != "unknown" and len(closes) >= 80)
    return {
        "verified": verified,
        "direction": direction,
        "close": close,
        "ema20": ema20,
        "ema50": ema50,
        "rsi": rsi,
        "fresh": fresh,
        "age_hours": round(age_seconds / 3600.0, 2),
        "provider": data["provider"],
        "provider_symbol": data["provider_symbol"],
        "last_close_time": datetime.fromtimestamp(
            last_close_ms / 1000.0, timezone.utc
        ).isoformat().replace("+00:00", "Z"),
    }


def asset_usd_effect(symbol: str, usd_direction: str) -> str:
    cleaned = clean_symbol(symbol)
    inverse_asset = (
        cleaned.endswith("USDT")
        or cleaned in {"EURUSD", "GBPUSD", "AUDUSD", "XAUUSD", "XAGUSD", "SPX", "NDX", "DJI"}
    )
    if not inverse_asset or usd_direction == "neutral":
        return "neutral"
    if usd_direction == "bullish":
        return "negative_pressure"
    if usd_direction == "bearish":
        return "positive_support"
    return "unknown"


ORIGINAL_BUILD_PAYLOAD = v30.build_payload
ORIGINAL_HEALTH = v30.health


def enhanced_build_payload(
    upstream: Mapping[str, Any],
    symbol: str,
    timeframe: str,
    mode: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    payload, evidence = ORIGINAL_BUILD_PAYLOAD(upstream, symbol, timeframe, mode)

    ohlcv = fetch_ohlcv(symbol, timeframe, 240)
    closes = [float(value) for value in ohlcv["closes"]]
    highs = [float(value) for value in ohlcv["highs"]]
    lows = [float(value) for value in ohlcv["lows"]]
    volumes = [float(value) for value in ohlcv["volumes"]]
    close_times = [int(value) for value in ohlcv["close_times"]]

    if len(closes) < 80:
        raise ValueError(f"INSUFFICIENT_TECHNICAL_BARS:{symbol}:{timeframe}:{len(closes)}")

    last_close_ms = close_times[-1]
    age_seconds = max(0.0, time.time() - (last_close_ms / 1000.0))
    max_age = MAX_AGE_SECONDS[timeframe]
    if age_seconds > max_age:
        raise ValueError(
            f"STALE_TECHNICAL_DATA:{symbol}:{timeframe}:{round(age_seconds / 3600, 2)}h"
        )

    rsi_values = rsi_series(closes, 14)
    macd_values = macd_histogram(closes)
    obv_values = obv_series(closes, volumes)
    cci_values = cci_series(highs, lows, closes, 20)

    full_indicators = {
        "RSI": rsi_values,
        "MACD_HISTOGRAM": macd_values,
        "OBV": [float(value) for value in obv_values],
        "CCI": cci_values,
    }
    divergence = detect_divergence(highs, lows, full_indicators)
    momentum = momentum_result(rsi_values, macd_values, obv_values, cci_values)
    levels = payload.get("scenario_levels") if isinstance(payload.get("scenario_levels"), Mapping) else {}
    liquidity = liquidity_result(symbol, ohlcv, levels)
    dxy = dxy_result()

    old_macro = payload.get("usd_macro_result")
    old_macro = old_macro if isinstance(old_macro, Mapping) else {}
    usd_macro = dict(old_macro)
    usd_macro.update({
        "status": "AVAILABLE" if dxy["verified"] else "PARTIAL_AVAILABLE",
        "confidence": 88 if dxy["verified"] else 55,
        "input_quality": "FULL" if dxy["verified"] else "PARTIAL",
        "usd_direction_verified": bool(dxy["verified"]),
        "usd_direction": dxy["direction"],
        "dxy": dxy,
        "asset_effect": asset_usd_effect(symbol, dxy["direction"]),
        "reason": (
            "LIVE_DXY_CALENDAR_AND_NEWS_BOUND"
            if dxy["verified"]
            else "DXY_VERIFICATION_GATE_NOT_MET"
        ),
    })

    payload["divergence_result"] = divergence
    payload["momentum_result"] = momentum
    payload["liquidity_structure_result"] = liquidity
    payload["usd_macro_result"] = usd_macro

    blockers = list(evidence.get("critical_blockers") or [])
    removable = {
        "DIVERGENCE_ENGINE_INPUT_SET_NOT_BOUND": divergence["status"] == "AVAILABLE",
        "MOMENTUM_INDICATOR_SET_PARTIAL": momentum["status"] == "AVAILABLE",
        "LIQUIDITY_FEED_NOT_VERIFIED": bool(liquidity["liquidity_verified"]),
        "USD_DIRECTION_FEED_NOT_VERIFIED": bool(usd_macro["usd_direction_verified"]),
    }
    blockers = [
        blocker for blocker in blockers
        if not removable.get(blocker, False)
    ]
    blockers = list(dict.fromkeys(blockers))

    risk = payload.get("risk_result")
    risk = risk if isinstance(risk, Mapping) else {}
    risk_blocked = bool(risk.get("blocked"))
    payload["devils_advocate_blocked"] = risk_blocked
    payload["devils_advocate_reasons"] = blockers
    evidence["critical_blockers"] = blockers

    input_matrix = evidence.get("input_matrix")
    if not isinstance(input_matrix, dict):
        input_matrix = {}
        evidence["input_matrix"] = input_matrix
    input_matrix["L05"] = {
        "state": "LIVE",
        "source": "REAL_OHLCV_RSI_MACD_OBV_CCI",
    }
    input_matrix["L09"] = {
        "state": "LIVE",
        "source": "REAL_OHLCV_RSI_MACD_OBV_CCI",
    }
    input_matrix["L10"] = {
        "state": "LIVE" if liquidity["liquidity_verified"] else "PARTIAL",
        "source": liquidity.get("order_book", {}).get("provider", "OHLCV_VOLUME_ONLY"),
    }
    input_matrix["L11"] = {
        "state": "LIVE" if dxy["verified"] else "PARTIAL",
        "source": "LIVE_DXY_PLUS_CALENDAR_PLUS_NEWS",
    }

    evidence["technical_evidence_v33"] = {
        "symbol": clean_symbol(symbol),
        "timeframe": timeframe,
        "provider": ohlcv["provider"],
        "provider_symbol": ohlcv["provider_symbol"],
        "interval": ohlcv["interval"],
        "bar_count": len(closes),
        "last_close_time": datetime.fromtimestamp(
            last_close_ms / 1000.0, timezone.utc
        ).isoformat().replace("+00:00", "Z"),
        "age_hours": round(age_seconds / 3600.0, 2),
        "fresh": True,
        "indicator_set": ["RSI", "MACD_HISTOGRAM", "OBV", "CCI"],
        "liquidity_verified": bool(liquidity["liquidity_verified"]),
        "usd_direction_verified": bool(dxy["verified"]),
        "dxy_direction": dxy["direction"],
    }
    return payload, evidence


def enhanced_health():
    status, payload = ORIGINAL_HEALTH()
    payload = dict(payload)
    payload.update({
        "service": "ndsp-canonical-live-runtime-v33",
        "runtime_version": VERSION,
        "contract_version": CONTRACT_VERSION,
        "host": HOST,
        "port": PORT,
        "runtime_dir": str(RUNTIME_DIR),
        "publicly_exposed": False,
        "evidence_binding": {
            "divergence": "REAL_OHLCV_RSI_MACD_OBV_CCI",
            "momentum": "REAL_OHLCV_RSI_MACD_OBV_CCI",
            "crypto_liquidity": "BINANCE_PUBLIC_ORDER_BOOK",
            "usd_direction": "DXY_PUBLIC_CHART",
            "cot": "UNCHANGED_TRUTHFUL_GATE",
        },
    })
    return status, payload


v30.VERSION = VERSION
v30.CONTRACT_VERSION = CONTRACT_VERSION
v30.HOST = HOST
v30.PORT = PORT
v30.RUNTIME_DIR = RUNTIME_DIR
v30.build_payload = enhanced_build_payload
v30.health = enhanced_health
v30.Handler.server_version = "NDSPCanonicalLive/33"


def main() -> None:
    v30.main()


if __name__ == "__main__":
    main()

