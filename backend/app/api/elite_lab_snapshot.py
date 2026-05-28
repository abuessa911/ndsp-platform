from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/v6/elite-lab", tags=["elite-lab"])

SUPPORTED_SYMBOLS = {
    "BTCUSDT": "Digital Assets",
    "ETHUSDT": "Digital Assets",
    "SOLUSDT": "Digital Assets",
    "EURUSD": "Currencies",
    "XAUUSD": "Metals",
    "USOIL": "Energy",
    "US30": "Equity Indices",
}


def safe_dict(value: Any) -> Any:
    try:
        if isinstance(value, dict):
            return value
        if hasattr(value, "model_dump"):
            return value.model_dump()
        if hasattr(value, "dict"):
            return value.dict()
        if hasattr(value, "__dict__"):
            return dict(value.__dict__)
        return value
    except Exception:
        return {"raw": str(value)}


def get_live_snapshot(symbol: str) -> dict:
    errors = []

    try:
        from app.services.price_router import get_market_snapshot
        try:
            data = get_market_snapshot(symbol)
        except TypeError:
            data = get_market_snapshot(market=symbol)
        return {
            "ok": True,
            "source": "app.services.price_router.get_market_snapshot",
            "data": safe_dict(data),
        }
    except Exception as exc:
        errors.append(f"price_router:{type(exc).__name__}:{exc}")

    try:
        from app.core.market_profile import resolve_market
        data = resolve_market(symbol)
        return {
            "ok": True,
            "source": "app.core.market_profile.resolve_market",
            "data": safe_dict(data),
        }
    except Exception as exc:
        errors.append(f"market_profile:{type(exc).__name__}:{exc}")

    return {
        "ok": False,
        "source": "unavailable",
        "data": {},
        "errors": errors[-5:],
    }


@router.get("/snapshot")
def elite_lab_snapshot(symbol: str = Query("BTCUSDT")) -> dict:
    symbol = symbol.upper().strip()
    if symbol not in SUPPORTED_SYMBOLS:
        symbol = "BTCUSDT"

    live = get_live_snapshot(symbol)

    return {
        "ok": True,
        "system": "NDSP",
        "mode": "Decision Support / Execution Sanitized",
        "symbol": symbol,
        "asset_class": SUPPORTED_SYMBOLS[symbol],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "live": live,
        "layers": [
            {"id": 1, "name": "Market Context", "public": "Reads broad market environment."},
            {"id": 2, "name": "Asset Classification", "public": "Classifies the selected asset."},
            {"id": 3, "name": "Live Data Surface", "public": "Displays available backend market data."},
            {"id": 4, "name": "Direction Context", "public": "Summarizes directional environment."},
            {"id": 5, "name": "Momentum Review", "public": "Reviews motion quality."},
            {"id": 6, "name": "Volatility Frame", "public": "Frames current instability."},
            {"id": 7, "name": "Risk Context", "public": "Shows risk awareness only."},
            {"id": 8, "name": "Conflict Check", "public": "Detects mixed conditions."},
            {"id": 9, "name": "Quality Filter", "public": "Filters weak context."},
            {"id": 10, "name": "Timing Context", "public": "Shows timing environment."},
            {"id": 11, "name": "Source Governance", "public": "Keeps source handling controlled."},
            {"id": 12, "name": "Decision Hygiene", "public": "Prevents raw logic exposure."},
            {"id": 13, "name": "Output Sanitization", "public": "Shows safe user-facing output."},
            {"id": 14, "name": "Explainability", "public": "Explains without exposing secrets."},
            {"id": 15, "name": "Operational Guardrails", "public": "No direct execution."},
            {"id": 16, "name": "SaaS Access Layer", "public": "Controls plan and trial access."},
        ],
    }
