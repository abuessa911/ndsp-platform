from __future__ import annotations

import os

SOURCE = os.getenv("NDSP_PRICE_SOURCE", "mt4").strip().lower()


def get_market_snapshot(symbol: str) -> dict:
    if SOURCE == "mt4":
        from app.services.mt4_market import get_market_snapshot as _get
        return _get(symbol)

    if SOURCE == "binance":
        from app.services.price_router import get_market_snapshot as _get
        return _get(symbol)

    from app.services.mt4_market import get_market_snapshot as _get
    return _get(symbol)


def get_price(symbol: str) -> float:
    snap = get_market_snapshot(symbol)
    try:
        return float(snap.get("price") or 0.0)
    except Exception:
        return 0.0
