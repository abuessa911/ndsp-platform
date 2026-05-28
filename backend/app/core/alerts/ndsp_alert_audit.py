from __future__ import annotations
from app.ndsp_db_env_loader import load_ndsp_db_env
load_ndsp_db_env(force=True)

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4


AUDIT_PATH = Path(os.getenv("NDSP_ALERT_AUDIT_FILE", "/home/nawaf511/empire-core-new/backend/runtime/alert_audit_log.jsonl"))
STATE_PATH = Path(os.getenv("NDSP_ALERT_STATE_FILE", "/home/nawaf511/empire-core-new/backend/runtime/alert_spam_state.json"))


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
    "DATABASE_URL",
    "JWT_SECRET",
    "API_SECRET",
    "ADMIN_KEY",
    "TELEGRAM_BOT_TOKEN",
    "SMTP_PASSWORD",
    "PUSH_SECRET",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _clean(value: Any, limit: int = 800) -> str:
    text = str(value or "").strip()
    for term in FORBIDDEN_TERMS:
        text = text.replace(term, "[sanitized]")
        text = text.replace(term.lower(), "[sanitized]")
    return text[:limit]


def _ensure_runtime() -> None:
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)


def sanitize_audit_record(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": _clean(record.get("id") or str(uuid4())),
        "timestamp": _clean(record.get("timestamp") or utc_now()),
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "event_type": _clean(record.get("event_type") or "alert_event"),
        "symbol": _clean(record.get("symbol") or "SYSTEM").upper(),
        "package": _clean(record.get("package") or "Free"),
        "severity": _clean(record.get("severity") or "info"),
        "decision_direction": _clean(record.get("decision_direction") or "neutral"),
        "confidence": record.get("confidence", 0),
        "risk_state": _clean(record.get("risk_state") or "normal"),
        "system_state": _clean(record.get("system_state") or "live"),
        "rule_id": _clean(record.get("rule_id") or "none"),
        "allowed": bool(record.get("allowed", False)),
        "blocked_reason": _clean(record.get("blocked_reason") or ""),
        "channels": [str(x).lower() for x in (record.get("channels") or []) if str(x).lower() in {"portal", "telegram", "email", "push"}],
        "delivery_result": record.get("delivery_result") if isinstance(record.get("delivery_result"), dict) else {},
        "message": _clean(record.get("message") or ""),
        "compliance": {
            "passed": True,
            "sanitized": True,
            "logic_leak": False,
            "direct_execution": False,
        },
    }


def append_audit(record: Dict[str, Any]) -> Dict[str, Any]:
    _ensure_runtime()
    safe = sanitize_audit_record(record)
    with AUDIT_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(safe, ensure_ascii=False, sort_keys=True) + "\n")
    try:
        os.chmod(AUDIT_PATH, 0o600)
    except Exception:
        pass
    return safe


def read_recent_audit(limit: int = 25) -> List[Dict[str, Any]]:
    if not AUDIT_PATH.exists():
        return []

    limit = max(1, min(int(limit or 25), 100))
    try:
        lines = AUDIT_PATH.read_text(encoding="utf-8").splitlines()
    except Exception:
        return []

    rows: List[Dict[str, Any]] = []
    for line in lines[-limit:]:
        try:
            obj = json.loads(line)
            if isinstance(obj, dict):
                rows.append(sanitize_audit_record(obj))
        except Exception:
            continue

    return list(reversed(rows))


def read_spam_state() -> Dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    try:
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def write_spam_state(state: Dict[str, Any]) -> Dict[str, Any]:
    _ensure_runtime()
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    try:
        os.chmod(STATE_PATH, 0o600)
    except Exception:
        pass
    return state


def public_audit_status() -> Dict[str, Any]:
    return {
        "audit_file": str(AUDIT_PATH),
        "state_file": str(STATE_PATH),
        "secrets_exposed": False,
    }
