from __future__ import annotations

import hmac
import os
from typing import Optional

from fastapi import APIRouter, Header, HTTPException, Request

from app.api.admin.payments_admin_v6 import admin_confirm_payment
from app.saas.subscriptions_db import save_audit_event

router = APIRouter(prefix="/api/v6/payments", tags=["payments-webhook-v6"])


def _expected_secret() -> str:
    return (
        os.getenv("PAYMENT_WEBHOOK_SECRET")
        or os.getenv("NDSP_PAYMENT_WEBHOOK_SECRET")
        or ""
    )


def _verify_secret(secret: Optional[str]) -> bool:
    expected = _expected_secret()

    if not expected:
        return False

    if not secret:
        return False

    return hmac.compare_digest(str(secret), str(expected))


@router.post("/webhook")
async def payment_webhook_v6(
    request: Request,
    x_ndsp_webhook_secret: Optional[str] = Header(default=None),
):
    if not _verify_secret(x_ndsp_webhook_secret):
        raise HTTPException(status_code=401, detail="Invalid webhook secret")

    payload = await request.json()

    event = payload.get("event") or payload.get("type") or "payment.confirmed"

    allowed_events = {
        "payment.confirmed",
        "payment_paid",
        "paid",
        "charge.paid",
        "invoice.paid",
    }

    if event not in allowed_events:
        save_audit_event(
            event_type="webhook_ignored",
            entity_type="payment_webhook",
            entity_id=str(payload.get("id") or payload.get("payment_ref") or ""),
            actor_type="webhook",
            actor_id=str(payload.get("provider") or "unknown"),
            message="Unsupported webhook event ignored",
            payload_json=str(payload),
        )

        return {
            "status": "ignored",
            "reason": "unsupported event",
            "event": event,
        }

    telegram_id = payload.get("telegram_id") or payload.get("telegram_user_id")
    email = payload.get("email")
    plan = payload.get("plan") or "pro"
    days = int(payload.get("days") or 30)
    payment_ref = payload.get("payment_ref") or payload.get("id") or payload.get("transaction_id")
    provider = payload.get("provider") or "webhook"
    amount = payload.get("amount")
    currency = payload.get("currency") or "USD"
    lead_id = payload.get("lead_id")

    if not telegram_id and not email:
        raise HTTPException(status_code=400, detail="telegram_id or email is required")

    if not payment_ref:
        raise HTTPException(status_code=400, detail="payment_ref is required")

    confirm_payload = {
        "telegram_id": str(telegram_id) if telegram_id else None,
        "email": email,
        "plan": plan,
        "days": days,
        "payment_ref": str(payment_ref),
        "provider": str(provider),
        "amount": str(amount) if amount is not None else None,
        "currency": currency,
        "create_invite": True,
        "source": "payment_webhook_v6",
    }

    if lead_id:
        confirm_payload["lead_id"] = lead_id

    save_audit_event(
        event_type="webhook_received",
        entity_type="payment_webhook",
        entity_id=str(payment_ref),
        actor_type="webhook",
        actor_id=str(provider),
        message="Payment webhook accepted",
        payload_json=str(payload),
    )

    result = admin_confirm_payment(confirm_payload)

    return {
        "status": "ok",
        "event": event,
        "result": result,
    }
