from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.services.price_sources import PriceSnapshot, resolve_market, source_order_for_market, utc_now_iso


CACHE_FILE = Path(os.getenv("NDSP_PRICE_CACHE_FILE", "/tmp/ndsp_price_last_good.json"))
MAX_STALE_SECONDS = int(os.getenv("NDSP_PRICE_MAX_STALE_SECONDS", "900"))
MAX_SOURCE_DEVIATION_PCT = float(os.getenv("NDSP_PRICE_MAX_SOURCE_DEVIATION_PCT", "3.0"))


def _load_cache() -> Dict[str, Any]:
    try:
        if CACHE_FILE.exists():
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def _save_cache(data: Dict[str, Any]) -> None:
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = CACHE_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(CACHE_FILE)
    except Exception:
        pass


def _cache_good(snapshot: PriceSnapshot) -> None:
    if not snapshot.ok or snapshot.price is None:
        return
    data = _load_cache()
    data[snapshot.symbol.upper()] = snapshot.dict()
    _save_cache(data)


def _last_good(symbol: str) -> Optional[PriceSnapshot]:
    data = _load_cache()
    item = data.get(symbol.upper())
    if not item:
        return None
    try:
        return PriceSnapshot(**item)
    except Exception:
        return None


def _quality_rank(q: str) -> int:
    return {
        "live": 100,
        "fallback_live": 85,
        "fallback_delayed": 60,
        "fallback_stale": 30,
        "last_good": 20,
        "unavailable": 0,
    }.get(q, 0)


def _deviation_pct(a: float, b: float) -> float:
    if not a or not b:
        return 999.0
    mid = (abs(a) + abs(b)) / 2
    if mid <= 0:
        return 999.0
    return abs(a - b) / mid * 100


def get_market_snapshot(symbol: str, market: Optional[str] = None, timeout: float = 5.0) -> Dict[str, Any]:
    symbol = symbol.upper().replace("/", "").replace("-", "")
    market = market or resolve_market(symbol)

    attempts: List[Dict[str, Any]] = []
    successful: List[PriceSnapshot] = []

    for src in source_order_for_market(market):
        if not src.supports(symbol, market):
            continue
        snap = src.fetch(symbol, market, timeout=timeout)
        attempts.append(snap.dict())
        if snap.ok and snap.price is not None:
            successful.append(snap)

    chosen: Optional[PriceSnapshot] = None
    warning = None

    if successful:
        successful = sorted(successful, key=lambda x: (_quality_rank(x.quality), -x.latency_ms), reverse=True)
        chosen = successful[0]

        if len(successful) >= 2:
            dev = _deviation_pct(float(successful[0].price), float(successful[1].price))
            if dev > MAX_SOURCE_DEVIATION_PCT:
                warning = f"source_deviation_above_threshold:{dev:.2f}%"
                if chosen.quality != "live":
                    chosen.quality = "fallback_delayed"

        if chosen.stale_seconds is not None and chosen.stale_seconds > MAX_STALE_SECONDS:
            warning = "source_stale_above_threshold"

        _cache_good(chosen)

    if chosen is None:
        cached = _last_good(symbol)
        if cached and cached.price is not None:
            cached.source = "database_last_good"
            cached.quality = "last_good"
            cached.fallback_used = True
            cached.reason = "all_sources_failed_using_last_good"
            chosen = cached
            warning = "all_sources_failed_last_good_used"

    system_state = "live"
    risk_state = "normal"
    data_quality = "live"

    if chosen is None:
        system_state = "safe_mode"
        risk_state = "paused"
        data_quality = "unavailable"
        return {
            "ok": False,
            "system": "NDSP",
            "version": "1.0.0",
            "governance_version": "6.1.0",
            "symbol": symbol,
            "market": market,
            "price": None,
            "price_source": None,
            "fallback_used": True,
            "source_health": "unsafe",
            "data_quality": data_quality,
            "system_state": system_state,
            "risk_state": risk_state,
            "timestamp": utc_now_iso(),
            "warning": "all_sources_failed",
            "attempts": attempts,
        }

    if chosen.quality == "live":
        source_health = "healthy"
        data_quality = "live"
    elif chosen.quality in {"fallback_live", "fallback_delayed"}:
        source_health = "degraded"
        data_quality = "protected"
    elif chosen.quality in {"fallback_stale", "last_good"}:
        source_health = "unsafe"
        data_quality = "stale"
        system_state = "safe_mode"
        risk_state = "paused"
    else:
        source_health = "unsafe"
        data_quality = "unavailable"
        system_state = "safe_mode"
        risk_state = "paused"

    primary_source_name = attempts[0]["source"] if attempts else None
    fallback_used = chosen.source != primary_source_name

    return {
        "ok": True,
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "symbol": symbol,
        "market": market,
        "price": chosen.price,
        "price_source": chosen.source,
        "raw_symbol": chosen.raw_symbol,
        "fallback_used": bool(fallback_used or chosen.fallback_used),
        "source_health": source_health,
        "data_quality": data_quality,
        "quality": chosen.quality,
        "latency_ms": chosen.latency_ms,
        "stale_seconds": chosen.stale_seconds,
        "system_state": system_state,
        "risk_state": risk_state,
        "timestamp": utc_now_iso(),
        "warning": warning,
        "attempts": attempts,
    }


def get_price_status(symbol: str) -> Dict[str, Any]:
    return get_market_snapshot(symbol)
