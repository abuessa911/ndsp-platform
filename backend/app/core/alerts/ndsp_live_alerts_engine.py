from __future__ import annotations
from app.ndsp_db_env_loader import load_ndsp_db_env
load_ndsp_db_env(force=True)

from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4


ALLOWED_SEVERITY = {"info", "watch", "warning", "critical"}
ALLOWED_CHANNELS = {"portal", "telegram", "email", "push"}
FORBIDDEN_TERMS = [
    "BUY NOW",
    "SELL NOW",
    "TP",
    "SL",
    "take profit",
    "stop loss",
    "raw_rsi",
    "raw_macd",
    "cot_raw",
    "admin_key",
    "DATABASE_URL",
    "JWT_SECRET",
    "API_SECRET",
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value: Any) -> str:
    text = str(value or "").strip()
    for term in FORBIDDEN_TERMS:
        text = text.replace(term, "[sanitized]")
        text = text.replace(term.lower(), "[sanitized]")
    return text[:600]


def sanitize_alert(alert: Dict[str, Any]) -> Dict[str, Any]:
    severity = str(alert.get("severity") or "info").lower()
    if severity not in ALLOWED_SEVERITY:
        severity = "info"

    channels = alert.get("channels") or ["portal"]
    if not isinstance(channels, list):
        channels = ["portal"]

    safe_channels: List[str] = []
    for ch in channels:
        c = str(ch).lower()
        if c in ALLOWED_CHANNELS and c not in safe_channels:
            safe_channels.append(c)

    if not safe_channels:
        safe_channels = ["portal"]

    symbol = _safe_text(alert.get("symbol") or "SYSTEM").upper()
    title = _safe_text(alert.get("title") or "NDSP Alert")
    message = _safe_text(alert.get("message") or "Governed decision-support update is available.")
    context = _safe_text(alert.get("context") or "Decision Active / Execution Sanitized")

    return {
        "id": str(alert.get("id") or uuid4()),
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "timestamp": str(alert.get("timestamp") or _now()),
        "symbol": symbol,
        "severity": severity,
        "title": title,
        "message": message,
        "context": context,
        "channels": safe_channels,
        "delivery_mode": "sanitized",
        "execution": {
            "mode": "Execution Sanitized",
            "direct_execution": False,
            "broker_action": False,
        },
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
        },
    }


def build_decision_alert(payload: Dict[str, Any]) -> Dict[str, Any]:
    decision = payload.get("decision") or {}
    states = payload.get("states") or {}
    risk = payload.get("risk") or {}
    market_alignment = payload.get("market_alignment") or {}
    intelligence = payload.get("intelligence") or {}
    momentum_dual = intelligence.get("momentum_dual") or {}

    symbol = payload.get("symbol") or "SYSTEM"
    direction = str(decision.get("direction") or "neutral").lower()
    confidence = decision.get("confidence", 0)
    system_state = states.get("system_state") or "live"
    risk_state = states.get("risk_state") or risk.get("state") or "normal"
    nmp_signal = market_alignment.get("signal") or "NO_SIGNAL"
    momentum_signal = momentum_dual.get("signal") or "NEUTRAL"

    severity = "info"
    if str(system_state).lower() in {"safe_mode", "blocked", "error"}:
        severity = "warning"
    if str(risk_state).lower() in {"paused", "drawdown"}:
        severity = "warning"
    try:
        if float(confidence) >= 80 and severity == "info":
            severity = "watch"
    except Exception:
        confidence = 0

    title = f"{symbol} Governed Decision Update"
    message = (
        f"Context: {direction}. Confidence: {confidence}. "
        f"Risk: {risk_state}. System: {system_state}."
    )
    context = (
        f"Decision Active / Execution Sanitized. "
        f"market_alignment context: {nmp_signal}. Momentum context: {momentum_signal}."
    )

    return sanitize_alert({
        "symbol": symbol,
        "severity": severity,
        "title": title,
        "message": message,
        "context": context,
        "channels": ["portal", "telegram", "email", "push"],
    })


def demo_alerts() -> List[Dict[str, Any]]:
    return [
        sanitize_alert({
            "symbol": "BTCUSDT",
            "severity": "watch",
            "title": "BTCUSDT Governed Context Update",
            "message": "A governed decision-support update is available with elevated confidence.",
            "context": "Decision Active / Execution Sanitized",
            "channels": ["portal", "telegram"],
        }),
        sanitize_alert({
            "symbol": "XAUUSD",
            "severity": "info",
            "title": "XAUUSD Market Context Refresh",
            "message": "Market context refreshed through the governed backend pipeline.",
            "context": "Sanitized output only. No execution command.",
            "channels": ["portal"],
        }),
    ]
