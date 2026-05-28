from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4

from app.core.alerts.ndsp_alert_audit import append_audit, read_recent_audit, read_spam_state, write_spam_state
from app.core.alerts.ndsp_live_alerts_engine import sanitize_alert
from app.core.delivery.ndsp_delivery_interfaces import deliver_alert


PACKAGE_CHANNELS = {
    "Free": ["portal"],
    "Pro": ["portal", "email"],
    "Elite": ["portal", "telegram", "email", "push"],
    "SaaS": ["portal", "telegram", "email", "push"],
}

PACKAGE_CONFIDENCE_MIN = {
    "Free": 80,
    "Pro": 72,
    "Elite": 65,
    "SaaS": 60,
}

DEFAULT_COOLDOWN_SECONDS = {
    "Free": 1800,
    "Pro": 900,
    "Elite": 300,
    "SaaS": 180,
}

ALLOWED_PACKAGES = {"Free", "Pro", "Elite", "SaaS"}
ALLOWED_DIRECTIONS = {"bullish", "bearish", "neutral"}
ALLOWED_RISK = {"normal", "paused", "drawdown"}
ALLOWED_SYSTEM = {"live", "safe_mode", "blocked", "error"}


def _now_dt() -> datetime:
    return datetime.now(timezone.utc)


def _now_iso() -> str:
    return _now_dt().isoformat()


def _package(value: Any) -> str:
    v = str(value or "Free").strip()
    return v if v in ALLOWED_PACKAGES else "Free"


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _decision_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    decision = payload.get("decision") or {}
    states = payload.get("states") or {}
    risk = payload.get("risk") or {}
    subscription = payload.get("subscription") or {}
    user = payload.get("user") or {}

    package = _package(
        payload.get("package")
        or subscription.get("plan")
        or subscription.get("current_plan")
        or user.get("package")
        or "Free"
    )

    direction = str(decision.get("direction") or "neutral").lower()
    if direction not in ALLOWED_DIRECTIONS:
        direction = "neutral"

    confidence = _safe_float(decision.get("confidence"), 0)

    risk_state = str(states.get("risk_state") or risk.get("state") or "normal").lower()
    if risk_state not in ALLOWED_RISK:
        risk_state = "normal"

    system_state = str(states.get("system_state") or "live").lower()
    if system_state not in ALLOWED_SYSTEM:
        system_state = "live"

    symbol = str(payload.get("symbol") or "SYSTEM").upper()

    return {
        "symbol": symbol,
        "package": package,
        "direction": direction,
        "confidence": confidence,
        "risk_state": risk_state,
        "system_state": system_state,
    }


def rules_snapshot() -> Dict[str, Any]:
    return {
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "mode": {
            "decision": "Decision Active",
            "execution": "Execution Sanitized",
        },
        "allowed_packages": sorted(ALLOWED_PACKAGES),
        "package_channels": PACKAGE_CHANNELS,
        "package_confidence_min": PACKAGE_CONFIDENCE_MIN,
        "cooldown_seconds": DEFAULT_COOLDOWN_SECONDS,
        "rules": [
            {
                "id": "risk_guard",
                "description": "Paused, drawdown, blocked, or error states do not trigger external delivery.",
            },
            {
                "id": "confidence_threshold",
                "description": "Minimum confidence is enforced by package.",
            },
            {
                "id": "neutral_guard",
                "description": "Neutral decision context is logged but not externally delivered unless risk/system state requires review.",
            },
            {
                "id": "spam_guard",
                "description": "Repeated symbol/package/direction alerts are blocked by cooldown.",
            },
        ],
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
            "direct_execution": False,
        },
    }


def spam_guard_key(fields: Dict[str, Any]) -> str:
    return f"{fields['package']}::{fields['symbol']}::{fields['direction']}::{fields['risk_state']}::{fields['system_state']}"


def check_spam_guard(fields: Dict[str, Any]) -> Dict[str, Any]:
    state = read_spam_state()
    key = spam_guard_key(fields)
    package = fields["package"]
    cooldown = int(DEFAULT_COOLDOWN_SECONDS.get(package, 900))

    now = _now_dt()
    last_iso = state.get(key)

    if last_iso:
        try:
            last = datetime.fromisoformat(str(last_iso))
            age = (now - last).total_seconds()
            if age < cooldown:
                return {
                    "allowed": False,
                    "reason": "spam_guard_cooldown",
                    "cooldown_seconds": cooldown,
                    "remaining_seconds": max(0, int(cooldown - age)),
                    "key": key,
                }
        except Exception:
            pass

    state[key] = now.isoformat()
    write_spam_state(state)

    return {
        "allowed": True,
        "reason": "allowed",
        "cooldown_seconds": cooldown,
        "remaining_seconds": 0,
        "key": key,
    }


def evaluate_rules(payload: Dict[str, Any], deliver: bool = False) -> Dict[str, Any]:
    fields = _decision_fields(payload)

    package = fields["package"]
    confidence_min = PACKAGE_CONFIDENCE_MIN.get(package, 80)
    channels = PACKAGE_CHANNELS.get(package, ["portal"])

    allowed = True
    blocked_reason = ""
    severity = "info"
    rule_id = "allowed"

    if fields["system_state"] in {"blocked", "error"}:
        allowed = False
        blocked_reason = "system_state_blocks_delivery"
        severity = "warning"
        rule_id = "risk_guard"
    elif fields["risk_state"] in {"paused", "drawdown"}:
        allowed = False
        blocked_reason = "risk_state_blocks_delivery"
        severity = "warning"
        rule_id = "risk_guard"
    elif fields["direction"] == "neutral":
        allowed = False
        blocked_reason = "neutral_context_logged_only"
        severity = "info"
        rule_id = "neutral_guard"
    elif fields["confidence"] < confidence_min:
        allowed = False
        blocked_reason = "confidence_below_package_threshold"
        severity = "info"
        rule_id = "confidence_threshold"

    spam = {"allowed": True, "reason": "not_checked"}
    if allowed:
        spam = check_spam_guard(fields)
        if not spam.get("allowed"):
            allowed = False
            blocked_reason = spam.get("reason") or "spam_guard_cooldown"
            severity = "info"
            rule_id = "spam_guard"

    if allowed and fields["confidence"] >= 85:
        severity = "watch"
    if allowed and fields["confidence"] >= 93:
        severity = "critical"

    title = f"{fields['symbol']} Governed Alert"
    message = (
        f"Sanitized {fields['direction']} decision-support context "
        f"with confidence {fields['confidence']:.0f} for {package} access."
    )
    context = "Decision Active / Execution Sanitized. No direct execution."

    alert = sanitize_alert({
        "symbol": fields["symbol"],
        "severity": severity,
        "title": title,
        "message": message,
        "context": context,
        "channels": channels if allowed else ["portal"],
    })

    delivery_result: Dict[str, Any] = {}
    if allowed and deliver:
        delivery_result = deliver_alert(alert)

    audit = append_audit({
        "event_type": "alert_rule_evaluation",
        "symbol": fields["symbol"],
        "package": package,
        "severity": severity,
        "decision_direction": fields["direction"],
        "confidence": fields["confidence"],
        "risk_state": fields["risk_state"],
        "system_state": fields["system_state"],
        "rule_id": rule_id,
        "allowed": allowed,
        "blocked_reason": blocked_reason,
        "channels": alert.get("channels") or [],
        "delivery_result": delivery_result,
        "message": message,
    })

    return {
        "ok": True,
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "decision_mode": "Decision Active",
        "execution_mode": "Execution Sanitized",
        "allowed": allowed,
        "blocked_reason": blocked_reason,
        "rule_id": rule_id,
        "fields": fields,
        "spam_guard": spam,
        "alert": alert,
        "delivery": delivery_result,
        "audit": audit,
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
            "direct_execution": False,
        },
    }


def recent_alerts(limit: int = 25) -> Dict[str, Any]:
    return {
        "ok": True,
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "decision_mode": "Decision Active",
        "execution_mode": "Execution Sanitized",
        "read_only": True,
        "alerts": read_recent_audit(limit=limit),
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
            "direct_execution": False,
        },
    }
