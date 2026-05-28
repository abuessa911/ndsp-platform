from __future__ import annotations

from fastapi import APIRouter, Query

from app.services.price_router import get_market_snapshot

router = APIRouter(tags=["price-status"])


@router.get("/price-status")
def price_status(symbol: str = Query("BTCUSDT", min_length=3, max_length=20)):
    snap = get_market_snapshot(symbol)
    return {
        "ok": snap.get("ok", False),
        "system": "NDSP",
        "version": snap.get("version", "1.0.0"),
        "governance_version": snap.get("governance_version", "6.1.0"),
        "symbol": snap.get("symbol"),
        "market": snap.get("market"),
        "price": snap.get("price"),
        "price_source": snap.get("price_source"),
        "fallback_used": snap.get("fallback_used"),
        "source_health": snap.get("source_health"),
        "data_quality": snap.get("data_quality"),
        "quality": snap.get("quality"),
        "latency_ms": snap.get("latency_ms"),
        "stale_seconds": snap.get("stale_seconds"),
        "system_state": snap.get("system_state"),
        "risk_state": snap.get("risk_state"),
        "timestamp": snap.get("timestamp"),
        "warning": snap.get("warning"),
    }
