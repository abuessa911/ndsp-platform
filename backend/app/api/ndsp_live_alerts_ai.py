from __future__ import annotations

import os
from typing import Any, Dict

from fastapi import APIRouter, Header, HTTPException

from app.core.alerts.ndsp_live_alerts_engine import build_decision_alert, demo_alerts, sanitize_alert
from app.core.alerts.ndsp_alert_rules_engine import evaluate_rules, recent_alerts, rules_snapshot
from app.core.assistant.ndsp_ai_assistant_layer import explain_alert, explain_payload
from app.core.delivery.ndsp_delivery_interfaces import deliver_alert, delivery_status
from app.core.delivery.ndsp_delivery_settings import public_settings_status, read_delivery_settings, write_delivery_settings


router = APIRouter(prefix="/api/v6/live", tags=["NDSP Live Alerts + AI Assistant"])


def _require_admin(x_admin_key: str | None) -> None:
    expected = os.getenv("ADMIN_KEY", "").strip()
    if not expected:
        raise HTTPException(status_code=503, detail="Admin controls unavailable")
    if not x_admin_key or x_admin_key != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/alerts")
def get_live_alerts() -> Dict[str, Any]:
    return {
        "ok": True,
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "mode": {
            "decision": "Decision Active",
            "execution": "Execution Sanitized",
        },
        "read_only": True,
        "alerts": demo_alerts(),
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
        },
    }


@router.get("/delivery/status")
def get_delivery_status() -> Dict[str, Any]:
    return {
        "ok": True,
        **delivery_status(),
    }


@router.post("/alerts/sanitize")
def public_sanitize_alert(payload: Dict[str, Any]) -> Dict[str, Any]:
    alert = sanitize_alert(payload)
    return {
        "ok": True,
        "alert": alert,
        "assistant": explain_alert(alert),
    }


@router.post("/assistant/explain")
def assistant_explain(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "ok": True,
        "assistant": explain_payload(payload),
    }


@router.post("/admin/alerts/test")
def admin_test_alert(payload: Dict[str, Any], x_admin_key: str | None = Header(default=None)) -> Dict[str, Any]:
    _require_admin(x_admin_key)

    alert = sanitize_alert(payload)
    delivery = deliver_alert(alert)

    return {
        "ok": True,
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "admin_action": "test_sanitized_alert",
        "alert": alert,
        "assistant": explain_alert(alert),
        "delivery": delivery,
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
            "admin_key_server_side_only": True,
        },
    }


@router.post("/admin/alerts/from-decision")
def admin_alert_from_decision(payload: Dict[str, Any], x_admin_key: str | None = Header(default=None)) -> Dict[str, Any]:
    _require_admin(x_admin_key)

    alert = build_decision_alert(payload)
    delivery = deliver_alert(alert)

    return {
        "ok": True,
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "admin_action": "decision_to_sanitized_alert",
        "alert": alert,
        "assistant": explain_payload(payload),
        "delivery": delivery,
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
            "admin_key_server_side_only": True,
        },
    }

@router.post("/admin/delivery/test")
def admin_delivery_test(payload: Dict[str, Any], x_admin_key: str | None = Header(default=None)) -> Dict[str, Any]:
    _require_admin(x_admin_key)

    alert = sanitize_alert({
        "symbol": payload.get("symbol") or "SYSTEM",
        "severity": payload.get("severity") or "watch",
        "title": payload.get("title") or "NDSP Delivery Channel Test",
        "message": payload.get("message") or "Governed sanitized delivery channel test.",
        "context": "Decision Active / Execution Sanitized",
        "channels": payload.get("channels") or ["portal"],
    })

    delivery = deliver_alert(alert)

    return {
        "ok": True,
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "admin_action": "delivery_channel_test",
        "alert": alert,
        "delivery": delivery,
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
            "admin_authorization_server_side_only": True,
            "direct_execution": False,
        },
    }

@router.get("/admin/delivery/settings")
def admin_get_delivery_settings(x_admin_key: str | None = Header(default=None)) -> Dict[str, Any]:
    _require_admin(x_admin_key)

    status = delivery_status()
    settings = read_delivery_settings()

    return {
        "ok": True,
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "settings": settings,
        "status": status,
        "settings_meta": public_settings_status(),
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
            "secrets_exposed": False,
            "admin_authorization_server_side_only": True,
            "direct_execution": False,
        },
    }


@router.post("/admin/delivery/settings")
def admin_update_delivery_settings(payload: Dict[str, Any], x_admin_key: str | None = Header(default=None)) -> Dict[str, Any]:
    _require_admin(x_admin_key)

    allowed = {}
    for channel in ("telegram", "email", "push"):
        if channel in payload:
            value = payload.get(channel) or {}
            allowed[channel] = {"enabled": bool(value.get("enabled", False))}

    settings = write_delivery_settings(allowed)
    status = delivery_status()

    return {
        "ok": True,
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "settings": settings,
        "status": status,
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
            "secrets_exposed": False,
            "admin_authorization_server_side_only": True,
            "direct_execution": False,
        },
    }

@router.get("/alerts/recent")
def get_recent_rule_alerts(limit: int = 25) -> Dict[str, Any]:
    return recent_alerts(limit=limit)


@router.get("/admin/alerts/rules")
def admin_get_alert_rules(x_admin_key: str | None = Header(default=None)) -> Dict[str, Any]:
    _require_admin(x_admin_key)
    return {
        "ok": True,
        "rules": rules_snapshot(),
        "recent": recent_alerts(limit=25),
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
            "admin_authorization_server_side_only": True,
            "direct_execution": False,
        },
    }


@router.post("/admin/alerts/evaluate")
def admin_evaluate_alert_rules(payload: Dict[str, Any], x_admin_key: str | None = Header(default=None)) -> Dict[str, Any]:
    _require_admin(x_admin_key)
    deliver = bool(payload.get("deliver", False))
    decision_payload = payload.get("payload") if isinstance(payload.get("payload"), dict) else payload
    return evaluate_rules(decision_payload, deliver=deliver)

