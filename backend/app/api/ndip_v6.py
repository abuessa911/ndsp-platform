from __future__ import annotations

from fastapi import APIRouter, Query

from app.core.governed_pipeline import run_governed
from app.contracts.ndip_v6 import validate_payload_or_failsafe
from app.mock.ndip_v6_demo import build_admin_overview

router = APIRouter(prefix="/api/v6", tags=["ndsp-v6"])


def _dashboard_payload_from_pipeline(symbol: str) -> dict:
    result = run_governed(symbol)

    return {
        "version": result.get("version", "1.0.0"),
        "symbol": result.get("symbol", symbol),
        "decision": result.get("decision", {
            "direction": "neutral",
            "confidence": 0,
        }),
        "market_alignment": result.get("market_alignment", {
            "signal": "NO_SIGNAL",
            "zone_context": "No sanitized market_alignment context available",
            "entry_effect": "No entry-quality adjustment applied",
        }),
        "scenario": result.get("scenario", {
            "interest": "No governed scenario available",
            "invalidation": "New governed decision required",
            "target": "Wait for clearer market structure",
        }),
        "states": result.get("states", {
            "system_state": "safe_mode",
            "risk_state": "paused",
            "position_state": "monitoring",
        }),
        "execution": result.get("execution", {
            "lifecycle": "monitoring",
            "trade_id": "00000000-0000-0000-0000-000000000000",
        }),
        "alerts": result.get("alerts", []),
        "history": result.get("history", []),
        "risk": result.get("risk", {
            "state": "paused",
            "reason": "Pipeline fallback",
        }),
        "meta": {
            "timestamp": result.get("meta", {}).get("timestamp"),
            "latency_ms": result.get("meta", {}).get("latency_ms", 0),
            "symbol_id": result.get("meta", {}).get("symbol_id", f"{symbol}-SPOT"),
            "connection_status": "connected",
        },
    }


@router.get("/dashboard")
def get_dashboard(symbol: str = Query(default="BTCUSDT")):
    payload = _dashboard_payload_from_pipeline(symbol=symbol)
    return validate_payload_or_failsafe(payload)


@router.get("/admin/overview")
def get_admin_overview():
    return build_admin_overview()
