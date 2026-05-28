from __future__ import annotations

import os
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v6/admin-console", tags=["admin-console-v6"])

SYSTEM = "NDSP"
VERSION = "1.0.0"
GOVERNANCE_VERSION = "6.1.0"

ALLOWED_PLANS = ["Free", "Pro", "Elite", "SaaS"]
ALLOWED_ACTIONS = ["confirm", "reject"]

DATA_DIR = Path(os.environ.get("NDSP_DATA_DIR", "/home/nawaf511/empire-core-new/backend/data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

PAYMENTS_FILE = DATA_DIR / "ndsp_admin_payments.json"
SUBSCRIPTIONS_FILE = DATA_DIR / "ndsp_admin_subscriptions.json"
AUDIT_FILE = DATA_DIR / "ndsp_admin_audit_log.json"
USER_SUBSCRIPTIONS_FILE = DATA_DIR / "ndsp_user_subscriptions.json"


class AdminDecisionRequest(BaseModel):
    payment_id: str = Field(..., min_length=1)
    action: str = Field(..., pattern="^(confirm|reject)$")
    plan: str = Field(..., pattern="^(Free|Pro|Elite|SaaS)$")
    email: Optional[str] = None
    note: Optional[str] = None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _request_id() -> str:
    return str(uuid.uuid4())


def _admin_key_candidates() -> List[str]:
    names = (
        "NDSP_ADMIN_KEY",
        "ADMIN_KEY",
        "ADMIN_API_KEY",
        "NDSP_ADMIN_API_KEY",
        "NDIP_ADMIN_KEY",
        "NDIP_ADMIN_API_KEY",
        "ADMIN_UI_KEY",
        "ADMIN_CONSOLE_KEY",
    )
    values: List[str] = []
    for name in names:
        value = os.environ.get(name, "")
        if value:
            clean = value.strip().strip('"').strip("'")
            if clean and clean not in values:
                values.append(clean)
    return values


def _admin_key() -> str:
    values = _admin_key_candidates()
    return values[0] if values else ""


def _require_admin(x_admin_key: Optional[str]) -> None:
    candidates = _admin_key_candidates()
    incoming = (x_admin_key or "").strip().strip('"').strip("'")

    if not candidates:
        raise HTTPException(status_code=503, detail="Admin security key is not configured on backend")

    if not incoming:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if incoming not in candidates:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/auth-debug")
def auth_debug(x_admin_key: Optional[str] = Header(default=None)):
    incoming = (x_admin_key or "").strip().strip('"').strip("'")
    candidates = _admin_key_candidates()
    return {
        "ok": True,
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "timestamp": _now(),
        "request_id": _request_id(),
        "incoming_header_present": bool(incoming),
        "incoming_header_length": len(incoming),
        "candidate_count": len(candidates),
        "candidate_lengths": [len(v) for v in candidates],
        "match": incoming in candidates if incoming else False,
        "secrets_exposed": False,
    }


def _read_json(path: Path, default: Any) -> Any:
    try:
        if not path.exists():
            return default
        raw = path.read_text(encoding="utf-8").strip()
        if not raw:
            return default
        return json.loads(raw)
    except Exception:
        return default


def _write_json(path: Path, payload: Any) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def _audit(event: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    logs = _read_json(AUDIT_FILE, [])
    if not isinstance(logs, list):
        logs = []
    item = {
        "id": _request_id(),
        "timestamp": _now(),
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "event": event,
        "payload": payload,
    }
    logs.insert(0, item)
    logs = logs[:500]
    _write_json(AUDIT_FILE, logs)
    return item


def _seed_if_empty() -> None:
    payments = _read_json(PAYMENTS_FILE, [])
    subscriptions = _read_json(SUBSCRIPTIONS_FILE, [])

    if not isinstance(payments, list) or len(payments) == 0:
        payments = [
            {
                "payment_id": "np_live_bridge_pending_001",
                "email": "pending-user@ndsp.app",
                "plan": "Pro",
                "amount": "49",
                "currency": "USD",
                "payment_status": "waiting_admin_review",
                "source": "nowpayments_subscription_status",
                "created_at": _now(),
                "updated_at": _now(),
            }
        ]
        _write_json(PAYMENTS_FILE, payments)

    if not isinstance(subscriptions, list) or len(subscriptions) == 0:
        subscriptions = [
            {
                "email": "pending-user@ndsp.app",
                "plan": "Pro",
                "status": "pending",
                "source": "nowpayments_subscription_status",
                "active": False,
                "updated_at": _now(),
            }
        ]
        _write_json(SUBSCRIPTIONS_FILE, subscriptions)



def _upsert_user_subscription(
    email: str,
    plan: str,
    active: bool,
    status: str,
    source: str,
    payment_id: str,
    note: str = "",
) -> Dict[str, Any]:
    email_key = (email or "").strip().lower()
    if not email_key:
        return {}

    rows = _read_json(USER_SUBSCRIPTIONS_FILE, [])
    if not isinstance(rows, list):
        rows = []

    found = None
    for row in rows:
        if str(row.get("email", "")).strip().lower() == email_key:
            found = row
            break

    if found is None:
        found = {
            "id": str(uuid.uuid4()),
            "email": email_key,
            "created_at": _now(),
        }
        rows.insert(0, found)

    found.update({
        "email": email_key,
        "plan": plan,
        "current_plan": plan,
        "active": active,
        "active_subscription": active,
        "status": status,
        "source": source,
        "last_payment_id": payment_id,
        "admin_note": note,
        "updated_at": _now(),
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
    })

    _write_json(USER_SUBSCRIPTIONS_FILE, rows)
    return found


@router.get("/user-subscription")
def user_subscription(email: str):
    email_key = (email or "").strip().lower()
    rows = _read_json(USER_SUBSCRIPTIONS_FILE, [])
    if not isinstance(rows, list):
        rows = []

    for row in rows:
        if str(row.get("email", "")).strip().lower() == email_key:
            return {
                "ok": True,
                "system": SYSTEM,
                "version": VERSION,
                "governance_version": GOVERNANCE_VERSION,
                "timestamp": _now(),
                "request_id": _request_id(),
                "subscription": row,
                "source": row.get("source", "admin_payment_state"),
            }

    return {
        "ok": True,
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "timestamp": _now(),
        "request_id": _request_id(),
        "subscription": {
            "email": email_key,
            "plan": "Free",
            "current_plan": "Free",
            "active": False,
            "active_subscription": False,
            "status": "free",
            "source": "default_free_fallback",
        },
        "source": "default_free_fallback",
    }


def _summary(payments: List[Dict[str, Any]], subscriptions: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_plan = {p: {"payments": 0, "subscriptions": 0, "active": 0, "locked_above": []} for p in ALLOWED_PLANS}

    for p in payments:
        plan = str(p.get("plan") or "Free")
        if plan in by_plan:
            by_plan[plan]["payments"] += 1

    for s in subscriptions:
        plan = str(s.get("plan") or "Free")
        if plan in by_plan:
            by_plan[plan]["subscriptions"] += 1
            if bool(s.get("active")) or str(s.get("status", "")).lower() == "active":
                by_plan[plan]["active"] += 1

    by_plan["Free"]["locked_above"] = ["Pro", "Elite", "SaaS"]
    by_plan["Pro"]["locked_above"] = ["Elite", "SaaS"]
    by_plan["Elite"]["locked_above"] = ["SaaS"]
    by_plan["SaaS"]["locked_above"] = []

    return {
        "allowed_plans": ALLOWED_PLANS,
        "by_plan": by_plan,
        "source": "backend_admin_console_bridge",
        "backend_is_source_of_truth": True,
    }


@router.get("/overview")
def overview(x_admin_key: Optional[str] = Header(default=None)):
    _require_admin(x_admin_key)
    _seed_if_empty()

    payments = _read_json(PAYMENTS_FILE, [])
    subscriptions = _read_json(SUBSCRIPTIONS_FILE, [])
    audit = _read_json(AUDIT_FILE, [])

    if not isinstance(payments, list):
        payments = []
    if not isinstance(subscriptions, list):
        subscriptions = []
    if not isinstance(audit, list):
        audit = []

    return {
        "ok": True,
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "timestamp": _now(),
        "request_id": _request_id(),
        "payments": payments[:200],
        "subscriptions": subscriptions[:200],
        "audit_log": audit[:100],
        "plan_access_summary": _summary(payments, subscriptions),
        "security": {
            "admin_key_exposed_to_frontend": False,
            "actions_require_backend_admin_validation": True,
            "ui_is_not_source_of_truth": True,
        },
    }


@router.post("/payment-decision")
def payment_decision(payload: AdminDecisionRequest, x_admin_key: Optional[str] = Header(default=None)):
    _require_admin(x_admin_key)
    _seed_if_empty()

    payments = _read_json(PAYMENTS_FILE, [])
    subscriptions = _read_json(SUBSCRIPTIONS_FILE, [])

    if not isinstance(payments, list):
        payments = []
    if not isinstance(subscriptions, list):
        subscriptions = []

    target = None
    for item in payments:
        if str(item.get("payment_id")) == payload.payment_id:
            target = item
            break

    if target is None:
        target = {
            "payment_id": payload.payment_id,
            "email": payload.email or "",
            "plan": payload.plan,
            "amount": "",
            "currency": "",
            "source": "manual_admin_decision",
            "created_at": _now(),
        }
        payments.insert(0, target)

    status = "confirmed" if payload.action == "confirm" else "rejected"
    active = payload.action == "confirm"

    target["payment_status"] = status
    target["plan"] = payload.plan
    if payload.email:
        target["email"] = payload.email
    target["updated_at"] = _now()
    target["admin_note"] = payload.note or ""

    email = str(target.get("email") or payload.email or "").strip().lower()
    if email:
        found_sub = None
        for sub in subscriptions:
            if str(sub.get("email", "")).strip().lower() == email:
                found_sub = sub
                break

        if found_sub is None:
            found_sub = {"email": email, "created_at": _now()}
            subscriptions.insert(0, found_sub)

        found_sub["plan"] = payload.plan
        found_sub["status"] = "active" if active else "rejected"
        found_sub["active"] = active
        found_sub["source"] = "nowpayments_subscription_status"
        found_sub["updated_at"] = _now()
        found_sub["last_payment_id"] = payload.payment_id

    _write_json(PAYMENTS_FILE, payments)
    _write_json(SUBSCRIPTIONS_FILE, subscriptions)

    user_subscription_state = {}
    if email:
        user_subscription_state = _upsert_user_subscription(
            email=email,
            plan=payload.plan,
            active=active,
            status=("active" if active else "rejected"),
            source=("admin_payment_confirm" if active else "admin_payment_reject"),
            payment_id=payload.payment_id,
            note=payload.note or "",
        )

    audit_item = _audit(
        "payment_" + payload.action,
        {
            "payment_id": payload.payment_id,
            "plan": payload.plan,
            "email": email,
            "result_status": status,
            "source": "admin_console",
            "admin_key_exposed": False,
        },
    )

    return {
        "ok": True,
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "timestamp": _now(),
        "request_id": _request_id(),
        "payment": target,
        "user_subscription_state": user_subscription_state,
        "audit": audit_item,
    }


@router.get("/audit-log")
def audit_log(x_admin_key: Optional[str] = Header(default=None)):
    _require_admin(x_admin_key)
    audit = _read_json(AUDIT_FILE, [])
    if not isinstance(audit, list):
        audit = []
    return {
        "ok": True,
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "timestamp": _now(),
        "request_id": _request_id(),
        "audit_log": audit[:300],
    }
