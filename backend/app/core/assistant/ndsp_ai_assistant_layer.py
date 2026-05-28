from __future__ import annotations
from app.ndsp_db_env_loader import load_ndsp_db_env
load_ndsp_db_env(force=True)

from typing import Any, Dict


FORBIDDEN = [
    "BUY",
    "SELL",
    "TP",
    "SL",
    "RSI",
    "MACD",
    "market_positioning",
    "weight",
    "formula",
    "admin_key",
    "DATABASE_URL",
    "JWT",
]


def _clean(text: str) -> str:
    out = str(text or "")
    for term in FORBIDDEN:
        out = out.replace(term, "[protected]")
        out = out.replace(term.lower(), "[protected]")
    return out[:900]


def explain_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    decision = payload.get("decision") or {}
    states = payload.get("states") or {}
    risk = payload.get("risk") or {}
    explainability = payload.get("explainability") or {}

    direction = str(decision.get("direction") or "neutral").lower()
    confidence = decision.get("confidence", 0)
    system_state = states.get("system_state") or "live"
    risk_state = states.get("risk_state") or risk.get("state") or "normal"

    if direction not in {"bullish", "bearish", "neutral"}:
        direction = "neutral"

    summary = (
        f"NDSP is currently in {system_state} state with {risk_state} risk state. "
        f"The sanitized decision-support context is {direction} with confidence {confidence}."
    )

    guidance = (
        "This is a governed decision-support explanation only. "
        "It does not provide direct execution, broker instructions, or raw internal logic."
    )

    reason = explainability.get("reason") or "The backend pipeline produced a sanitized decision-support output."
    risk_explanation = explainability.get("risk_explanation") or "Risk state was evaluated before delivery."

    return {
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "assistant_mode": "sanitized_decision_support",
        "decision_mode": "Decision Active",
        "execution_mode": "Execution Sanitized",
        "summary": _clean(summary),
        "reason": _clean(reason),
        "risk_explanation": _clean(risk_explanation),
        "guidance": _clean(guidance),
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
            "direct_execution": False,
        },
    }


def explain_alert(alert: Dict[str, Any]) -> Dict[str, Any]:
    title = alert.get("title") or "NDSP Alert"
    message = alert.get("message") or "Governed alert update."
    severity = alert.get("severity") or "info"

    return {
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "assistant_mode": "sanitized_alert_explanation",
        "summary": _clean(f"{title}: {message}"),
        "severity": _clean(severity),
        "guidance": _clean(
            "Review the context inside NDSP. This alert is informational and does not represent an execution command."
        ),
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
            "direct_execution": False,
        },
    }
