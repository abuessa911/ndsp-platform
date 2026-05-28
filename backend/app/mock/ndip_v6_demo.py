from __future__ import annotations
from datetime import datetime, timezone, timedelta

def _iso_now():
    return datetime.now(timezone.utc)

def build_payload(symbol: str = "BTCUSDT", mode: str = "live") -> dict:
    now = _iso_now()
    base = {
        "version": "1.0.0",
        "symbol": symbol,
        "decision": {"direction": "bullish", "confidence": 78},
        "market_alignment": {
            "signal": "CONTINUATION_SIGNAL",
            "zone_context": "Institutional zone holding above reclaim area",
            "entry_effect": "Improves entry quality without changing direction",
            "explanation": "Sanitized market_alignment context available"
        },
        "scenario": {
            "interest": "Acceptance above the active decision zone",
            "invalidation": "Loss of decision support context",
            "target": "Continuation toward the monitored expansion area"
        },
        "states": {
            "system_state": "live",
            "risk_state": "normal",
            "position_state": "monitoring"
        },
        "execution": {
            "lifecycle": "monitoring",
            "trade_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        },
        "alerts": [
            {
                "type": "info",
                "priority": 2,
                "message": "Decision context refreshed successfully",
                "timestamp": now.isoformat()
            }
        ],
        "history": [
            {"direction": "neutral", "confidence": 51, "timestamp": (now - timedelta(hours=3)).isoformat()},
            {"direction": "bullish", "confidence": 78, "timestamp": now.isoformat()}
        ],
        "risk": {
            "state": "normal",
            "reason": "No active governance risk constraints"
        },
        "meta": {
            "timestamp": now.isoformat(),
            "latency_ms": 142,
            "symbol_id": f"{symbol}-SPOT",
            "connection_status": "connected"
        }
    }

    if mode == "paused":
        base["states"]["risk_state"] = "paused"
        base["risk"]["state"] = "paused"
        base["risk"]["reason"] = "Risk controls temporarily paused decision delivery"
        base["decision"]["confidence"] = 62
    elif mode == "drawdown":
        base["states"]["risk_state"] = "drawdown"
        base["risk"]["state"] = "drawdown"
        base["risk"]["reason"] = "Drawdown protection active"
        base["states"]["system_state"] = "blocked"
    elif mode == "safe_mode":
        base["states"]["system_state"] = "safe_mode"
        base["meta"]["connection_status"] = "degraded"
        base["risk"]["reason"] = "System stability fallback engaged"
    elif mode == "disconnected":
        base["states"]["system_state"] = "error"
        base["meta"]["connection_status"] = "disconnected"
        base["alerts"].append({
            "type": "critical",
            "priority": 1,
            "message": "Live feed disconnected",
            "timestamp": now.isoformat()
        })
    elif mode == "invalid":
        del base["meta"]["symbol_id"]

    return base

def build_admin_overview() -> dict:
    now = _iso_now().isoformat()
    return {
        "timestamp": now,
        "system_status": {
            "runtime": "healthy",
            "governance": "enforced",
            "compliance": "active",
        },
        "latency": {
            "p50_ms": 118,
            "p95_ms": 241,
            "feed_status": "connected",
        },
        "risk_triggers": [
            {"name": "drawdown_protection", "state": "idle"},
            {"name": "payload_validation", "state": "active"},
        ],
        "logs_summary": {
            "errors_24h": 2,
            "warnings_24h": 7,
        }
    }
