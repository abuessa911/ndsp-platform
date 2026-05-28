from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import APIRouter, Query

from app.core.governed_pipeline import run_governed

router = APIRouter(tags=["scanner-v1"])

PROJECT_ROOT = Path(__file__).resolve().parents[3]
WATCHLIST_FILE = PROJECT_ROOT / "runtime" / "fxcm_watchlist.txt"


def _read_watchlist(limit: int = 25) -> list[str]:
    symbols: list[str] = []

    if WATCHLIST_FILE.exists():
        for raw in WATCHLIST_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
            symbol = raw.strip().upper()
            if not symbol or symbol.startswith("#"):
                continue
            if symbol not in symbols:
                symbols.append(symbol)

    if not symbols:
        symbols = ["EURUSD", "USDCHF", "XAUUSD"]

    return symbols[: max(1, min(limit, 50))]


def _compact_decision(result: dict[str, Any]) -> dict[str, Any]:
    decision = result.get("decision") or {}
    meta = result.get("meta") or {}
    market = meta.get("market") or {}
    risk = result.get("risk") or {}
    states = result.get("states") or {}

    return {
        "symbol": result.get("symbol") or meta.get("symbol_id"),
        "direction": decision.get("direction", "neutral"),
        "confidence": decision.get("confidence", 0),
        "risk_state": risk.get("state") or states.get("risk_state"),
        "system_state": states.get("system_state"),
        "market_source": market.get("source"),
        "price": market.get("price"),
        "timestamp": meta.get("timestamp"),
        "pipeline_version": meta.get("pipeline_version"),
    }


def _scan(limit: int = 25) -> dict[str, Any]:
    symbols = _read_watchlist(limit=limit)
    items: list[dict[str, Any]] = []

    for symbol in symbols:
        try:
            result = run_governed(symbol=symbol)
            items.append(_compact_decision(result))
        except Exception as exc:
            items.append({
                "symbol": symbol,
                "direction": "neutral",
                "confidence": 0,
                "risk_state": "error",
                "system_state": "error",
                "market_source": None,
                "price": None,
                "timestamp": None,
                "pipeline_version": None,
                "error": str(exc),
            })

    bullish = sum(1 for item in items if item.get("direction") == "bullish")
    bearish = sum(1 for item in items if item.get("direction") == "bearish")
    neutral = sum(1 for item in items if item.get("direction") == "neutral")

    return {
        "version": "scanner_v1",
        "governance_version": "6.0.0",
        "source": "governed_pipeline",
        "watchlist_file": str(WATCHLIST_FILE),
        "count": len(items),
        "summary": {
            "bullish": bullish,
            "bearish": bearish,
            "neutral": neutral,
        },
        "items": items,
        "note": "Scanner uses governed pipeline only. It does not create a parallel decision path.",
    }


@router.get("/scanner")
def scanner(limit: int = Query(default=25, ge=1, le=50)):
    return _scan(limit=limit)


@router.get("/api/v6/scanner", include_in_schema=False)
def scanner_v6(limit: int = Query(default=25, ge=1, le=50)):
    return _scan(limit=limit)


@router.get("/api/v6/watchlist", include_in_schema=False)
def watchlist(limit: int = Query(default=25, ge=1, le=50)):
    symbols = _read_watchlist(limit=limit)
    return {
        "version": "watchlist_v1",
        "watchlist_file": str(WATCHLIST_FILE),
        "count": len(symbols),
        "symbols": symbols,
    }
