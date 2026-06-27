"""
NDSP compatibility module: app.core.market_positioning

Purpose:
- Keeps legacy/support imports working after moving layer logic.
- Provides safe neutral market-positioning helpers.
- Does not execute trades or override official L1-L16 decision pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class MarketPositioning:
    symbol: str = "UNKNOWN"
    bias: str = "NEUTRAL"
    confidence: float = 0.0
    source: str = "compat_market_positioning"
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "bias": self.bias,
            "confidence": self.confidence,
            "source": self.source,
            "details": self.details or {},
        }


def normalize_bias(value: Any) -> str:
    text = str(value or "").strip().upper()
    if text in {"BULLISH", "LONG", "BUY", "POSITIVE", "UP"}:
        return "BULLISH"
    if text in {"BEARISH", "SHORT", "SELL", "NEGATIVE", "DOWN"}:
        return "BEARISH"
    return "NEUTRAL"


def get_market_positioning(symbol: str = "UNKNOWN", data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Dict[str, Any]:
    data = data or {}
    raw_bias = (
        kwargs.get("bias")
        or data.get("bias")
        or data.get("direction")
        or data.get("signal")
        or data.get("state")
        or "NEUTRAL"
    )

    confidence = kwargs.get("confidence", data.get("confidence", data.get("score", 0.0)))
    try:
        confidence = float(confidence)
    except Exception:
        confidence = 0.0

    confidence = max(0.0, min(1.0, confidence))

    return MarketPositioning(
        symbol=symbol or data.get("symbol") or "UNKNOWN",
        bias=normalize_bias(raw_bias),
        confidence=confidence,
        details=data,
    ).to_dict()


def evaluate_market_positioning(symbol: str = "UNKNOWN", data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Dict[str, Any]:
    return get_market_positioning(symbol=symbol, data=data, **kwargs)


def compute_market_positioning(symbol: str = "UNKNOWN", data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Dict[str, Any]:
    return get_market_positioning(symbol=symbol, data=data, **kwargs)


def market_positioning_status() -> Dict[str, Any]:
    return {
        "ok": True,
        "module": "app.core.market_positioning",
        "mode": "compatibility_safe_neutral",
    }
