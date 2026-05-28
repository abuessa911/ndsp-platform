from __future__ import annotations

from typing import Any, Dict

from app.services.price_router import get_market_snapshot


def enrich_decision_with_price_router(payload: Dict[str, Any], symbol: str) -> Dict[str, Any]:
    """
    Public-safe market enrichment.

    This function does not decide direction.
    It only attaches sanitized market data quality/source status and applies safe_mode
    when the market data quality is unsafe/stale/unavailable.
    """
    if not isinstance(payload, dict):
        return payload

    try:
        snap = get_market_snapshot(symbol)
    except Exception:
        snap = {
            "ok": False,
            "system": "NDSP",
            "version": "1.0.0",
            "governance_version": "6.1.0",
            "symbol": symbol,
            "market": "unknown",
            "price": None,
            "price_source": None,
            "fallback_used": True,
            "source_health": "unsafe",
            "data_quality": "unavailable",
            "quality": "unavailable",
            "system_state": "safe_mode",
            "risk_state": "paused",
            "warning": "price_router_exception",
        }

    meta = payload.setdefault("meta", {})
    if not isinstance(meta, dict):
        meta = {}
        payload["meta"] = meta

    old_market = meta.get("market") if isinstance(meta.get("market"), dict) else {}

    meta["market"] = {
        **old_market,
        "source": snap.get("price_source"),
        "price": snap.get("price"),
        "asset_class": snap.get("market"),
        "data_quality": snap.get("data_quality"),
        "source_health": snap.get("source_health"),
        "quality": snap.get("quality"),
        "fallback_used": snap.get("fallback_used"),
        "latency_ms": snap.get("latency_ms"),
        "stale_seconds": snap.get("stale_seconds"),
        "warning": snap.get("warning"),
        "checked_at": snap.get("timestamp"),
        "router": "ndsp_redundant_price_router",
    }

    # Never force direction. Only protect output state if data quality is unsafe.
    unsafe = (
        not snap.get("ok")
        or snap.get("source_health") == "unsafe"
        or snap.get("data_quality") in {"stale", "unavailable"}
        or snap.get("system_state") == "safe_mode"
    )

    if unsafe:
        states = payload.setdefault("states", {})
        if isinstance(states, dict):
            states["system_state"] = "safe_mode"
            states["risk_state"] = "paused"

        risk = payload.setdefault("risk", {})
        if isinstance(risk, dict):
            risk["state"] = "paused"
            risk["reason"] = "Market data quality is unsafe; protected fallback/safe mode activated."

        decision = payload.setdefault("decision", {})
        if isinstance(decision, dict):
            decision["direction"] = "neutral"
            current_conf = decision.get("confidence", 0)
            try:
                decision["confidence"] = min(int(current_conf), 25)
            except Exception:
                decision["confidence"] = 25

        execution = payload.setdefault("execution", {})
        if isinstance(execution, dict):
            execution["direct_execution"] = False
            execution["public_command"] = False
            execution["execution_policy"] = "EXECUTION_SANITIZED"

    compliance = payload.setdefault("compliance", {})
    if isinstance(compliance, dict):
        compliance["market_data_sanitized"] = True
        compliance["price_router_attached"] = True
        compliance["direct_trade_execution"] = False
        compliance["logic_leak"] = False

    return payload
