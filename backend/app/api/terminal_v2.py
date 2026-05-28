from __future__ import annotations

from datetime import datetime, timezone
from math import isfinite
from typing import Any

from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/v6/terminal", tags=["terminal-v2"])

SUPPORTED = {
    "BTCUSDT": {"name": "Bitcoin", "class": "Digital Assets", "route": "binance"},
    "ETHUSDT": {"name": "Ethereum", "class": "Digital Assets", "route": "binance"},
    "SOLUSDT": {"name": "Solana", "class": "Digital Assets", "route": "binance"},
    "EURUSD": {"name": "EUR/USD", "class": "Currencies", "route": "mt4_fxcm"},
    "XAUUSD": {"name": "Gold", "class": "Metals", "route": "mt4_fxcm"},
    "USOIL": {"name": "US Oil", "class": "Energy", "route": "mt4_fxcm"},
    "US30": {"name": "Dow Jones", "class": "Equity Indices", "route": "mt4_fxcm"},
}

LAYER_NAMES = [
    "Market Context",
    "Asset Classification",
    "Live Data Surface",
    "Direction Context",
    "Momentum Review",
    "Volatility Frame",
    "Risk Context",
    "Conflict Check",
    "Quality Filter",
    "Timing Context",
    "Source Governance",
    "Decision Hygiene",
    "Output Sanitization",
    "Explainability",
    "Operational Guardrails",
    "SaaS Access Layer",
]


def _safe_dict(value: Any) -> dict:
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "dict"):
        return value.dict()
    if hasattr(value, "__dict__"):
        return dict(value.__dict__)
    return {}


def _deep_find(obj: Any, keys: list[str]) -> Any:
    if not isinstance(obj, dict):
        return None
    for key in keys:
        if key in obj and obj[key] not in (None, ""):
            return obj[key]
    for value in obj.values():
        if isinstance(value, dict):
            found = _deep_find(value, keys)
            if found not in (None, ""):
                return found
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    found = _deep_find(item, keys)
                    if found not in (None, ""):
                        return found
    return None


def _num(value: Any, default: float = 0.0) -> float:
    try:
        n = float(value)
        return n if isfinite(n) else default
    except Exception:
        return default


def _candles(data: dict) -> list[dict]:
    found = _deep_find(data, ["candles", "ohlcv"])
    if isinstance(found, list):
        return [x for x in found if isinstance(x, dict)][-80:]
    return []


def _market_snapshot(symbol: str) -> tuple[bool, str, dict, list[str]]:
    errors: list[str] = []

    try:
        from app.services.price_router import get_market_snapshot
        snap = get_market_snapshot(symbol)
        data = _safe_dict(snap)
        return True, str(data.get("source") or "price_router"), data, errors
    except Exception as exc:
        errors.append(f"price_router:{type(exc).__name__}")

    return False, "unavailable", {}, errors


def _regime(price: float, open_price: float, high: float, low: float) -> str:
    if not price or not open_price:
        return "neutral"
    move = (price - open_price) / open_price * 100
    spread = abs(high - low) / price * 100 if price and high and low else 0
    if move > 0.35 and spread < 3:
        return "constructive"
    if move < -0.35 and spread < 3:
        return "defensive"
    if spread >= 3:
        return "volatile"
    return "neutral"


def _risk(regime: str, live_ok: bool, candles_count: int) -> str:
    if not live_ok:
        return "safe_mode"
    if candles_count < 10:
        return "limited_visibility"
    if regime == "volatile":
        return "elevated"
    if regime in {"constructive", "defensive"}:
        return "normal"
    return "balanced"


def _confidence(live_ok: bool, candles_count: int, source: str) -> int:
    score = 40
    if live_ok:
        score += 25
    if candles_count >= 50:
        score += 20
    elif candles_count >= 10:
        score += 10
    if source not in {"unavailable", ""}:
        score += 10
    return max(0, min(95, score))


def _layer_states(live_ok: bool, confidence: int, regime: str, risk: str) -> list[dict]:
    states = []
    for idx, name in enumerate(LAYER_NAMES, start=1):
        if idx in {3, 11}:
            status = "active" if live_ok else "watch"
        elif idx in {7, 15}:
            status = "watch" if risk in {"elevated", "safe_mode"} else "active"
        elif idx in {8, 9}:
            status = "active" if confidence >= 60 else "watch"
        else:
            status = "active"
        states.append({
            "id": idx,
            "name": name,
            "status": status,
            "weight": max(35, min(95, confidence - (idx % 4) * 3)),
            "public_note": "Participating in governed decision-support synthesis.",
        })
    return states


@router.get("/snapshot")
def terminal_v2_snapshot(symbol: str = Query("BTCUSDT")) -> dict:
    symbol = symbol.upper().strip()
    if symbol not in SUPPORTED:
        symbol = "BTCUSDT"

    info = SUPPORTED[symbol]
    live_ok, source, raw, errors = _market_snapshot(symbol)
    candles = _candles(raw)

    last = candles[-1] if candles else {}
    price = _num(_deep_find(raw, ["price", "last", "close", "bid", "ask"]) or last.get("close") or last.get("price"))
    open_price = _num(_deep_find(raw, ["open"]) or last.get("open") or price)
    high = _num(_deep_find(raw, ["high"]) or last.get("high") or price)
    low = _num(_deep_find(raw, ["low"]) or last.get("low") or price)
    volume = _num(_deep_find(raw, ["volume", "vol"]) or last.get("volume") or 0)

    regime = _regime(price, open_price, high, low)
    risk_state = _risk(regime, live_ok, len(candles))
    confidence = _confidence(live_ok, len(candles), source)
    layers = _layer_states(live_ok, confidence, regime, risk_state)

    source_health = {
        "primary": source,
        "expected_route": info["route"],
        "live_ok": live_ok,
        "candles": len(candles),
        "errors": errors,
    }

    if live_ok:
        summary = (
            f"{symbol} is connected through {source}. The terminal is presenting a "
            f"{regime} market regime with {risk_state} risk state and {confidence}% confidence. "
            "All outputs remain decision-support only and execution-sanitized."
        )
    else:
        summary = (
            f"{symbol} source is not fully available. Terminal remains in protected "
            "monitoring mode. No execution output is exposed."
        )

    return {
        "ok": True,
        "system": "NDSP",
        "version": "terminal_v2",
        "mode": "Decision Active / Execution Sanitized",
        "symbol": symbol,
        "asset": info,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "market": {
            "price": price,
            "open": open_price,
            "high": high,
            "low": low,
            "volume": volume,
            "candles_count": len(candles),
            "source": source,
            "live_ok": live_ok,
        },
        "source_health": source_health,
        "decision": {
            "market_regime": regime,
            "risk_state": risk_state,
            "confidence": confidence,
            "summary": summary,
            "signal": "decision_support_only",
        },
        "layers": layers,
        "visual": {
            "candles": [
                {
                    "open": _num(c.get("open")),
                    "high": _num(c.get("high")),
                    "low": _num(c.get("low")),
                    "close": _num(c.get("close") or c.get("price")),
                    "volume": _num(c.get("volume")),
                }
                for c in candles[-48:]
            ],
        },
    }
