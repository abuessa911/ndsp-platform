from __future__ import annotations

import hashlib
import hmac
import json
import os
from typing import Optional

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Request, Query

from app.governance.admin_only import require_admin_role
from app.api.admin.payments_admin_v6 import admin_confirm_payment
from app.integrations.crypto.nowpayments_v6 import create_payment
from app.alerts.telegram_sender import send_telegram_to_chat




router = APIRouter(prefix="/api/v6/payments/nowpayments", tags=["nowpayments-v6"])


def ipn_secret() -> str:
    return os.getenv("NOWPAYMENTS_IPN_SECRET", "")


def verify_ipn_signature(raw_body: bytes, signature: Optional[str]) -> bool:
    secret = ipn_secret()

    if not secret:
        return False

    if not signature:
        return False

    digest = hmac.new(
        secret.encode("utf-8"),
        raw_body,
        hashlib.sha512,
    ).hexdigest()

    return hmac.compare_digest(digest, str(signature))




def parse_ndsp_order_id(order_id: str) -> dict:
    data = {}

    if not order_id:
        return data

    for part in str(order_id).split("|"):
        if "=" in part:
            key, value = part.split("=", 1)
            data[key.strip()] = value.strip()

    return data


def is_confirmed_status(status: str) -> bool:
    return status.lower() in {
        "finished",
        "confirmed",
        "sending",
        "paid",
        "partially_paid",
    }


@router.post("/create", dependencies=[Depends(require_admin_role)])
def admin_create_nowpayments_payment(payload: dict = Body(default={})):
    telegram_id = payload.get("telegram_id") or payload.get("telegram_user_id")
    lead_id = payload.get("lead_id")
    plan = payload.get("plan", "elite")
    days = int(payload.get("days", 30))
    amount = str(payload.get("amount", "99"))
    currency = payload.get("currency", "usd")
    pay_currency = payload.get("pay_currency", "usdttrc20")

    if not telegram_id:
        raise HTTPException(status_code=400, detail="telegram_id is required")

    order_id = payload.get("order_id") or f"ndsp|tg={telegram_id}|plan={plan}|days={days}|lead={lead_id or ''}"

    payment = create_payment(
        price_amount=amount,
        price_currency=currency,
        pay_currency=pay_currency,
        order_id=order_id,
        order_description=f"NDSP {plan} subscription",
        telegram_id=str(telegram_id),
        plan=str(plan),
        days=days,
        lead_id=str(lead_id) if lead_id else None,
    )

    payment_delivery = None

    try:
        pay_amount = payment.get("pay_amount")
        pay_currency = payment.get("pay_currency")
        pay_address = payment.get("pay_address")
        network = payment.get("network")
        valid_until = payment.get("valid_until")
        payment_id = payment.get("payment_id")

        if pay_address:
            message = "\n".join(
                [
                    "💳 NDSP USDT Payment Created",
                    "",
                    f"Plan: {plan}",
                    f"Days: {days}",
                    "",
                    f"Amount: {pay_amount} {pay_currency}",
                    f"Network: {network}",
                    "",
                    "Payment address:",
                    str(pay_address),
                    "",
                    f"Payment ID: {payment_id}",
                    f"Valid until: {valid_until}",
                    "",
                    "After payment is confirmed, your subscription will activate automatically.",
                ]
            )

            send_telegram_to_chat(str(telegram_id), message)

            payment_delivery = {
                "status": "sent",
                "telegram_id": str(telegram_id),
            }

    except Exception as exc:
        payment_delivery = {
            "status": "failed",
            "telegram_id": str(telegram_id),
            "error": str(exc),
        }

    return {
        "status": "ok",
        "provider": "nowpayments",
        "payment": payment,
        "payment_delivery": payment_delivery,
    }



# ==================================================
# NDSP PAYMENT REVIEW POLICY
# NOWPayments beta layer:
# Webhook confirms payment state only.
# No automatic subscription activation.
# Admin manual confirm is required.
# ==================================================
PAYMENT_REVIEW_STATUS = "pending_review"
PAYMENT_AUTO_ACTIVATION_ENABLED = False

def ndsp_payment_review_payload(provider_payload: dict, order_id: str | None = None, payment_id: str | None = None):
    try:
        status = str(provider_payload.get("payment_status") or provider_payload.get("status") or "unknown").lower()
    except Exception:
        status = "unknown"

    return {
        "status": "ok",
        "provider": "nowpayments",
        "mode": "beta_manual_review",
        "activation": "manual_review_required",
        "auto_activation": False,
        "review_status": PAYMENT_REVIEW_STATUS,
        "payment_status": status,
        "payment_id": payment_id or provider_payload.get("payment_id"),
        "order_id": order_id or provider_payload.get("order_id"),
        "message": "Payment webhook received. Subscription is pending manual admin review.",
    }

@router.post("/webhook")
async def nowpayments_webhook(
    request: Request,
    x_nowpayments_sig: Optional[str] = Header(default=None, alias="x-nowpayments-sig"),
):
    """
    NOWPayments webhook endpoint.

    NDSP Beta Payment Policy:
    - Receive provider status.
    - Record payment as pending_review.
    - Never activate subscription automatically.
    - Admin manual confirm is required.
    """
    try:
        payload = {}

        try:
            payload = await request.json()
        except Exception:
            payload = {}

        if not isinstance(payload, dict):
            payload = {"raw": str(payload)}

        payment_id = payload.get("payment_id")
        order_id = payload.get("order_id")
        payment_status = str(payload.get("payment_status") or payload.get("status") or "unknown").lower()

        review_payload = ndsp_payment_review_payload(
            provider_payload=payload,
            order_id=order_id,
            payment_id=payment_id,
        )

        try:
            save_audit_event(
                "nowpayments_webhook_pending_review",
                {
                    "payment_id": payment_id,
                    "order_id": order_id,
                    "payment_status": payment_status,
                    "review_status": "pending_review",
                    "auto_activation": False,
                    "payload": payload,
                },
            )
        except Exception:
            pass


        # webhook_pending_review_ledger_append_marker
        try:
            extracted = ndsp_extract_public_payment_from_order(order_id)
            ndsp_append_payment_ledger({
                "event_type": "payment_webhook",
                "review_status": "pending_review",
                "activation": "manual_review_required",
                "auto_activation": False,
                "email": extracted.get("email"),
                "telegram_id": extracted.get("telegram_id"),
                "plan": extracted.get("plan"),
                "network": extracted.get("network"),
                "days": extracted.get("days"),
                "payment_id": payment_id,
                "payment_status": payment_status,
                "order_id": order_id,
                "payload": payload,
            })
        except Exception:
            pass

        return review_payload

    except Exception as exc:
        try:
            save_audit_event(
                "nowpayments_webhook_error",
                {
                    "error": str(exc),
                    "review_status": "pending_review",
                    "auto_activation": False,
                },
            )
        except Exception:
            pass

        return {
            "status": "error",
            "provider": "nowpayments",
            "mode": "beta_manual_review",
            "activation": "manual_review_required",
            "auto_activation": False,
            "review_status": "pending_review",
            "message": "Webhook received but could not be fully processed. Manual review required.",
        }



# ==================================================
# NDSP ADMIN PAYMENTS LEDGER - Beta Layer
# Temporary JSONL ledger until PostgreSQL billing
# tables are finalized.
# ==================================================
def ndsp_payments_ledger_path():
    import os
    audit_dir = os.environ.get("NDSP_AUDIT_DIR", "/tmp/ndsp_audit")
    os.makedirs(audit_dir, exist_ok=True)
    return os.path.join(audit_dir, "payments_admin_ledger.jsonl")

def ndsp_append_payment_ledger(event: dict):
    try:
        import json
        from datetime import datetime, timezone

        if not isinstance(event, dict):
            event = {"raw": str(event)}

        event.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
        event.setdefault("system", "NDSP")
        event.setdefault("provider", "nowpayments")

        with open(ndsp_payments_ledger_path(), "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False, default=str) + "\n")

        return True
    except Exception:
        return False

def ndsp_read_payment_ledger(limit: int = 200):
    import json
    from pathlib import Path

    p = Path(ndsp_payments_ledger_path())
    if not p.exists():
        return []

    rows = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            rows.append({"raw": line})

    rows = rows[-int(limit):]
    rows.reverse()
    return rows

def ndsp_admin_key_ok(x_admin_key: str | None = None):
    import os
    import hmac

    provided = str(x_admin_key or "").strip()
    if not provided:
        return False

    for name in ("NDSP_ADMIN_KEY", "ADMIN_KEY", "ADMIN_API_KEY"):
        expected = str(os.environ.get(name) or "").strip()
        if expected and hmac.compare_digest(provided, expected):
            return True

    return False


def ndsp_public_payment_record_from_response(response: dict):
    try:
        req = response.get("request") or {}
        pay = response.get("payment") or {}
        return {
            "event_type": "payment_created",
            "review_status": "waiting_payment",
            "activation": "manual_review_required",
            "auto_activation": False,
            "email": req.get("email"),
            "telegram_id": req.get("telegram_id"),
            "plan": req.get("plan"),
            "network": req.get("network"),
            "days": req.get("days"),
            "payment_id": pay.get("payment_id"),
            "payment_status": pay.get("payment_status"),
            "pay_address": pay.get("pay_address"),
            "price_amount": pay.get("price_amount"),
            "price_currency": pay.get("price_currency"),
            "pay_amount": pay.get("pay_amount"),
            "pay_currency": pay.get("pay_currency"),
            "order_id": pay.get("order_id"),
            "purchase_id": pay.get("purchase_id"),
            "valid_until": pay.get("valid_until"),
        }
    except Exception:
        return {"event_type": "payment_created_parse_error"}

def ndsp_extract_public_payment_from_order(order_id: str | None):
    data = {
        "email": None,
        "telegram_id": None,
        "plan": None,
        "days": None,
        "network": None,
    }

    if not order_id:
        return data

    try:
        parts = str(order_id).split("|")
        for part in parts:
            if part.startswith("email="):
                data["email"] = part.split("=", 1)[1] or None
            elif part.startswith("tg="):
                data["telegram_id"] = part.split("=", 1)[1] or None
            elif part.startswith("plan="):
                data["plan"] = part.split("=", 1)[1] or None
            elif part.startswith("days="):
                data["days"] = part.split("=", 1)[1] or None
            elif part.startswith("network="):
                data["network"] = part.split("=", 1)[1] or None
    except Exception:
        pass

    return data


# ==================================================
# NDSP PUBLIC PAYMENT CONSTANTS - Beta Layer
# Safe defaults for NOWPayments public-create.
# ==================================================
if "PUBLIC_PLAN_PRICES_USD" not in globals():
    PUBLIC_PLAN_PRICES_USD = {
        "pro": 29,
        "elite": 99,
        "saas": 499,
    }

if "PUBLIC_PLAN_DAYS" not in globals():
    PUBLIC_PLAN_DAYS = {
        "pro": 30,
        "elite": 30,
        "saas": 30,
    }

if "_public_pay_currency" not in globals():
    def _public_pay_currency(network: str) -> str:
        n = str(network or "TRC20").upper().strip()
        if n == "TRC20":
            return "usdttrc20"
        if n == "BEP20":
            return "usdtbsc"
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_network",
                "allowed": ["TRC20", "BEP20"],
            },
        )

@router.post("/public-create")
async def public_create_nowpayments_payment(request: Request):
    """
    Public NOWPayments create payment endpoint.

    Reads JSON directly from Request to avoid Pydantic ForwardRef issues.
    Beta policy: manual review only, no auto activation.
    """
    try:
        try:
            payload = await request.json()
        except Exception:
            payload = {}

        if not isinstance(payload, dict):
            payload = {}

        email = str(payload.get("email") or "").strip().lower()
        telegram_id = str(payload.get("telegram_id") or "").strip() or None
        plan = str(payload.get("plan") or "").lower().strip()
        network = str(payload.get("network") or "TRC20").upper().strip()

        if not email or "@" not in email:
            raise HTTPException(status_code=422, detail="invalid_email")

        if plan not in PUBLIC_PLAN_PRICES_USD:
            raise HTTPException(status_code=400, detail="unsupported plan")

        amount = PUBLIC_PLAN_PRICES_USD[plan]
        days = PUBLIC_PLAN_DAYS.get(plan, 30) if hasattr(PUBLIC_PLAN_DAYS, "get") else 30
        pay_currency = _public_pay_currency(network)

        order_id = "|".join([
            "ndsp_public",
            f"email={email}",
            f"tg={telegram_id or ''}",
            f"plan={plan}",
            f"days={days}",
            f"network={network}",
        ])

        payment = create_payment(
            telegram_id=telegram_id or f"email:{email}",
            plan=plan,
            days=days,
            price_amount=amount,
            price_currency="usd",
            pay_currency=pay_currency,
            order_id=order_id,
            order_description=f"NDSP {plan.upper()} Beta Subscription",
        )

        if not isinstance(payment, dict):
            payment = {"raw": str(payment)}

        public_payment = {
            "payment_id": payment.get("payment_id"),
            "payment_status": payment.get("payment_status"),
            "pay_address": payment.get("pay_address"),
            "price_amount": payment.get("price_amount") or amount,
            "price_currency": payment.get("price_currency") or "usd",
            "pay_amount": payment.get("pay_amount"),
            "pay_currency": payment.get("pay_currency") or pay_currency,
            "network": payment.get("network") or network,
            "order_id": payment.get("order_id") or order_id,
            "expiration_estimate_date": payment.get("expiration_estimate_date"),
            "valid_until": payment.get("valid_until"),
            "purchase_id": payment.get("purchase_id"),
        }

        response_payload = {
            "status": "ok",
            "provider": "nowpayments",
            "mode": "beta_manual_review",
            "activation": "manual_review_required",
            "policy": {
                "currency": "USDT only",
                "networks": ["TRC20", "BEP20"],
                "confirmation": "webhook_verification_plus_manual_admin_review",
                "auto_activation": False,
            },
            "request": {
                "email": email,
                "telegram_id": telegram_id,
                "plan": plan,
                "network": network,
                "days": days,
            },
            "payment": public_payment,
        }

        try:
            save_audit_event(
                event_type="payment_request_created",
                entity_type="nowpayments_public_payment",
                entity_id=str(payment.get("payment_id") or ""),
                actor_type="user",
                actor_id=email,
                message="Public NOWPayments payment request created",
                payload_json=json.dumps(
                    {
                        "email": email,
                        "telegram_id": telegram_id,
                        "plan": plan,
                        "network": network,
                        "amount": amount,
                        "currency": "USD",
                        "payment_id": payment.get("payment_id"),
                        "status": payment.get("payment_status"),
                        "source": "public_nowpayments_create",
                        "auto_activation": False,
                    },
                    ensure_ascii=False,
                ),
            )
        except Exception:
            pass

        try:
            ndsp_append_payment_ledger(ndsp_public_payment_record_from_response(response_payload))
        except Exception:
            pass

        return response_payload

    except HTTPException:
        raise

    except Exception as exc:
        try:
            save_audit_event(
                "nowpayments_public_create_error",
                {"error": str(exc), "source": "public_create", "auto_activation": False},
            )
        except Exception:
            pass

        raise HTTPException(
            status_code=500,
            detail={
                "error": "payment_create_failed",
                "message": str(exc),
            },
        )


# ==================================================
# NDSP SUBSCRIPTION STATUS HELPERS - Beta Manual Layer
# ==================================================
def ndsp_latest_subscription_by_email(email: str):
    email = str(email or "").strip().lower()
    if not email:
        return None

    rows = ndsp_read_payment_ledger(limit=1000)
    latest = None

    # ndsp_read_payment_ledger returns newest first.
    for row in rows:
        if str(row.get("email") or "").strip().lower() != email:
            continue

        event_type = row.get("event_type")
        review_status = row.get("review_status")
        subscription_status = row.get("subscription_status")

        if event_type in ("admin_confirm", "admin_reject") or review_status in ("confirmed", "rejected") or subscription_status:
            latest = row
            break

    return latest

def ndsp_payment_event_by_id_or_email(payment_id: str | None = None, email: str | None = None):
    rows = ndsp_read_payment_ledger(limit=1000)
    payment_id = str(payment_id or "").strip()
    email = str(email or "").strip().lower()

    for row in rows:
        row_pid = str(row.get("payment_id") or "").strip()
        row_email = str(row.get("email") or "").strip().lower()

        if payment_id and row_pid == payment_id:
            return row

        if email and row_email == email:
            return row

    return None

@router.get("/subscription/status")
def nowpayments_subscription_status(email: str = Query(...)):
    email = str(email or "").strip().lower()

    if not email or "@" not in email:
        raise HTTPException(status_code=422, detail="invalid_email")

    latest = ndsp_latest_subscription_by_email(email)

    if not latest:
        return {
            "status": "ok",
            "email": email,
            "subscription_status": "inactive",
            "review_status": "none",
            "plan": None,
            "source": "none",
        }

    return {
        "status": "ok",
        "email": email,
        "subscription_status": latest.get("subscription_status") or "inactive",
        "review_status": latest.get("review_status"),
        "plan": latest.get("plan"),
        "payment_id": latest.get("payment_id"),
        "activation": latest.get("activation"),
        "auto_activation": False,
        "subscription_started_at": latest.get("subscription_started_at"),
        "subscription_expires_at": latest.get("subscription_expires_at"),
        "source": latest.get("source") or latest.get("event_type"),
    }


@router.get("/admin/list")
def admin_list_nowpayments_payments(x_admin_key: str | None = Header(default=None), limit: int = 200):
    if not ndsp_admin_key_ok(x_admin_key):
        raise HTTPException(status_code=401, detail="unauthorized")

    rows = ndsp_read_payment_ledger(limit=limit)

    return {
        "status": "ok",
        "provider": "nowpayments",
        "mode": "beta_manual_review",
        "auto_activation": False,
        "count": len(rows),
        "payments": rows,
    }

@router.post("/admin/confirm")
def admin_confirm_nowpayments_payment(payload: dict, x_admin_key: str | None = Header(default=None)):
    if not ndsp_admin_key_ok(x_admin_key):
        raise HTTPException(status_code=401, detail="unauthorized")

    payment_id = str(payload.get("payment_id") or "").strip()
    email = str(payload.get("email") or "").strip().lower()
    plan = str(payload.get("plan") or "").strip().lower()
    days = payload.get("days", 30)
    note = payload.get("note") or "Manual admin confirmation"

    existing = ndsp_payment_event_by_id_or_email(payment_id=payment_id, email=email)

    if not email and existing:
        email = str(existing.get("email") or "").strip().lower()

    if not plan and existing:
        plan = str(existing.get("plan") or "").strip().lower()

    if not payment_id and existing:
        payment_id = str(existing.get("payment_id") or "").strip()

    if not email:
        raise HTTPException(status_code=400, detail="email_required")

    if not plan:
        plan = "pro"

    try:
        days = int(days or 30)
    except Exception:
        days = 30

    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(days=days)

    event = {
        "event_type": "admin_confirm",
        "review_status": "confirmed",
        "subscription_status": "active",
        "activation": "manual_admin_confirmed",
        "auto_activation": False,
        "payment_id": payment_id,
        "email": email,
        "plan": plan,
        "days": days,
        "confirmed_at": now.isoformat(),
        "subscription_started_at": now.isoformat(),
        "subscription_expires_at": expires_at.isoformat(),
        "note": note,
        "source": "admin_confirm",
    }

    ndsp_append_payment_ledger(event)

    try:
        save_audit_event("nowpayments_admin_confirm", event)
    except Exception:
        pass

    return {
        "status": "ok",
        "provider": "nowpayments",
        "review_status": "confirmed",
        "subscription_status": "active",
        "activation": "manual_admin_confirmed",
        "auto_activation": False,
        "payment_id": payment_id,
        "email": email,
        "plan": plan,
        "days": days,
        "subscription_started_at": event["subscription_started_at"],
        "subscription_expires_at": event["subscription_expires_at"],
    }

@router.post("/admin/reject")
def admin_reject_nowpayments_payment(payload: dict, x_admin_key: str | None = Header(default=None)):
    if not ndsp_admin_key_ok(x_admin_key):
        raise HTTPException(status_code=401, detail="unauthorized")

    payment_id = str(payload.get("payment_id") or "").strip()
    email = str(payload.get("email") or "").strip().lower()
    plan = str(payload.get("plan") or "").strip().lower()
    reason = payload.get("reason") or "Payment rejected by admin"

    existing = ndsp_payment_event_by_id_or_email(payment_id=payment_id, email=email)

    if not email and existing:
        email = str(existing.get("email") or "").strip().lower()

    if not plan and existing:
        plan = str(existing.get("plan") or "").strip().lower()

    if not payment_id and existing:
        payment_id = str(existing.get("payment_id") or "").strip()

    if not email:
        raise HTTPException(status_code=400, detail="email_required")

    if not plan:
        plan = "pro"

    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)

    event = {
        "event_type": "admin_reject",
        "review_status": "rejected",
        "subscription_status": "inactive",
        "activation": "manual_admin_rejected",
        "auto_activation": False,
        "payment_id": payment_id,
        "email": email,
        "plan": plan,
        "rejected_at": now.isoformat(),
        "reason": reason,
        "source": "admin_reject",
    }

    ndsp_append_payment_ledger(event)

    try:
        save_audit_event("nowpayments_admin_reject", event)
    except Exception:
        pass

    return {
        "status": "ok",
        "provider": "nowpayments",
        "review_status": "rejected",
        "subscription_status": "inactive",
        "activation": "manual_admin_rejected",
        "auto_activation": False,
        "payment_id": payment_id,
        "email": email,
        "plan": plan,
        "reason": reason,
    }
