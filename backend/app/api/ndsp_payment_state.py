from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
import json
import os
from pathlib import Path

router = APIRouter(prefix="/api/v6", tags=["ndsp-payment-state"])

SYSTEM = "NDSP"
VERSION = "1.0.0"
GOVERNANCE_VERSION = os.getenv("NDSP_GOVERNANCE_VERSION", "6.1.0")
DATA_DIR = Path(os.getenv("NDSP_STATE_DIR", "/var/lib/ndsp"))
PAYMENTS_FILE = DATA_DIR / "payments_state.json"
AUDIT_FILE = DATA_DIR / "audit_log.jsonl"


def now():
    return datetime.now(timezone.utc).isoformat()


def ensure_files():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not PAYMENTS_FILE.exists():
        PAYMENTS_FILE.write_text(json.dumps({"payments": {}, "subscriptions": {}}, ensure_ascii=False, indent=2), encoding="utf-8")
    if not AUDIT_FILE.exists():
        AUDIT_FILE.touch()


def read_state():
    ensure_files()
    try:
        return json.loads(PAYMENTS_FILE.read_text(encoding="utf-8") or "{}")
    except Exception:
        return {"payments": {}, "subscriptions": {}}


def write_state(data):
    ensure_files()
    tmp = PAYMENTS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(PAYMENTS_FILE)


def admin_ok(x_admin_key: Optional[str]) -> bool:
    expected = os.getenv("ADMIN_KEY", "").strip()
    return bool(expected and x_admin_key and x_admin_key.strip() == expected)


def audit(event, status, extra=None):
    ensure_files()
    row = {
        "timestamp": now(),
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "event": event,
        "status": status,
        "extra": extra or {},
    }
    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


class PaymentAction(BaseModel):
    payment_id: str
    note: Optional[str] = None


@router.get("/subscription/status")
def subscription_status(email: str):
    data = read_state()
    normalized = email.strip().lower()
    sub = data.get("subscriptions", {}).get(normalized)

    if not sub:
        sub = {
            "email": normalized,
            "plan": "Free",
            "current_plan": "Free",
            "active": False,
            "active_subscription": False,
            "status": "free",
            "source": "default_free_fallback",
        }

    return {
        "ok": True,
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "subscription": sub,
    }


@router.get("/payments")
def list_payments(x_admin_key: Optional[str] = Header(None)):
    if not admin_ok(x_admin_key):
        raise HTTPException(status_code=401, detail="unauthorized")

    data = read_state()
    return {
        "ok": True,
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "payments": list(data.get("payments", {}).values()),
    }


@router.post("/payments/confirm")
def confirm_payment(payload: PaymentAction, x_admin_key: Optional[str] = Header(None)):
    if not admin_ok(x_admin_key):
        raise HTTPException(status_code=401, detail="unauthorized")

    data = read_state()
    payments = data.setdefault("payments", {})
    subscriptions = data.setdefault("subscriptions", {})

    payment = payments.get(payload.payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="payment_not_found")

    if payment.get("status") == "confirmed":
        audit("payment_confirm_skipped_duplicate", "confirmed", {"payment_id": payload.payment_id})
        return {"ok": True, "changed": False, "reason": "already_confirmed", "payment": payment}

    if payment.get("status") == "rejected":
        audit("payment_confirm_blocked_rejected", "rejected", {"payment_id": payload.payment_id})
        return {"ok": False, "changed": False, "reason": "payment_already_rejected", "payment": payment}

    email = str(payment.get("user_email") or payment.get("email") or "").strip().lower()
    plan = payment.get("plan") or "Elite"

    payment["status"] = "confirmed"
    payment["confirmed_at"] = now()
    payment["updated_at"] = now()

    if email:
        subscriptions[email] = {
            "email": email,
            "plan": plan,
            "current_plan": plan,
            "active": True,
            "active_subscription": True,
            "status": "confirmed",
            "source": "confirmed_payment",
            "payment_id": payload.payment_id,
            "confirmed_at": payment["confirmed_at"],
        }

    write_state(data)
    audit("payment_confirmed", "confirmed", {"payment_id": payload.payment_id, "email": email, "plan": plan})

    return {"ok": True, "changed": True, "payment": payment, "subscription": subscriptions.get(email)}


@router.post("/payments/reject")
def reject_payment(payload: PaymentAction, x_admin_key: Optional[str] = Header(None)):
    if not admin_ok(x_admin_key):
        raise HTTPException(status_code=401, detail="unauthorized")

    data = read_state()
    payments = data.setdefault("payments", {})
    payment = payments.get(payload.payment_id)

    if not payment:
        raise HTTPException(status_code=404, detail="payment_not_found")

    if payment.get("status") == "rejected":
        audit("payment_reject_skipped_duplicate", "rejected", {"payment_id": payload.payment_id})
        return {"ok": True, "changed": False, "reason": "already_rejected", "payment": payment}

    if payment.get("status") == "confirmed":
        audit("payment_reject_blocked_confirmed", "confirmed", {"payment_id": payload.payment_id})
        return {"ok": False, "changed": False, "reason": "payment_already_confirmed", "payment": payment}

    payment["status"] = "rejected"
    payment["rejected_at"] = now()
    payment["updated_at"] = now()

    write_state(data)
    audit("payment_rejected", "rejected", {"payment_id": payload.payment_id})

    return {"ok": True, "changed": True, "payment": payment}


@router.post("/audit/cleanup")
def cleanup_audit_log(x_admin_key: Optional[str] = Header(None)):
    if not admin_ok(x_admin_key):
        raise HTTPException(status_code=401, detail="unauthorized")

    ensure_files()

    if not AUDIT_FILE.exists():
        return {
            "ok": True,
            "system": SYSTEM,
            "version": VERSION,
            "governance_version": GOVERNANCE_VERSION,
            "removed": 0,
            "kept": 0,
        }

    lines = AUDIT_FILE.read_text(encoding="utf-8").splitlines()
    seen = set()
    kept = []
    removed = 0

    dedupe_events = {
        "payment_confirmed",
        "payment_rejected",
        "nowpayments_admin_confirm",
        "nowpayments_admin_reject",
        "payment_confirm_skipped_duplicate",
        "payment_reject_skipped_duplicate",
        "payment_confirm_blocked_rejected",
        "payment_reject_blocked_confirmed",
        "audit_log_cleaned",
    }

    for line in lines:
        if not line.strip():
            continue

        try:
            rec = json.loads(line)
        except Exception:
            kept.append(line)
            continue

        event = str(rec.get("event") or rec.get("event_type") or "")
        status = str(rec.get("status") or rec.get("review_status") or "")
        extra = rec.get("extra") or {}

        payment_id = (
            rec.get("payment_id")
            or extra.get("payment_id")
            or rec.get("invoice_id")
            or extra.get("invoice_id")
            or rec.get("lead_id")
            or extra.get("lead_id")
            or "unknown"
        )

        email = (
            rec.get("email")
            or rec.get("user_email")
            or extra.get("email")
            or extra.get("user_email")
            or "unknown"
        )

        if event in dedupe_events:
            key = (event, status, str(payment_id), str(email))
            if key in seen:
                removed += 1
                continue
            seen.add(key)

        kept.append(json.dumps(rec, ensure_ascii=False, sort_keys=True))

    AUDIT_FILE.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")

    audit("audit_log_cleaned", "completed", {"removed": removed, "kept": len(kept)})

    return {
        "ok": True,
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "removed": removed,
        "kept": len(kept),
    }
