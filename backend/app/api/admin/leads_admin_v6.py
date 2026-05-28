from __future__ import annotations

from fastapi import APIRouter, Depends, Body, Query, HTTPException

from app.governance.admin_only import require_admin_role
from app.saas.subscriptions_db import (
    get_subscription_lead_by_id,
    list_subscription_leads,
    mark_subscription_lead_status,
)
from app.api.admin.payments_admin_v6 import admin_confirm_payment

router = APIRouter(prefix="/api/admin/leads", tags=["leads-admin"])


@router.get("", dependencies=[Depends(require_admin_role)])
def admin_list_leads(status: str | None = Query(default=None)):
    return {
        "status": "ok",
        "leads": list_subscription_leads(status=status),
    }


@router.post("/status", dependencies=[Depends(require_admin_role)])
def admin_update_lead_status(payload: dict = Body(default={})):
    lead_id = payload.get("lead_id")
    status = payload.get("status")

    if not lead_id:
        raise HTTPException(status_code=400, detail="lead_id is required")

    if status not in ("pending", "contacted", "paid", "cancelled"):
        raise HTTPException(status_code=400, detail="invalid status")

    lead = mark_subscription_lead_status(int(lead_id), status)

    return {
        "status": "ok",
        "lead": lead,
    }


@router.post("/mark-paid", dependencies=[Depends(require_admin_role)])
def admin_mark_lead_paid(payload: dict = Body(default={})):
    lead_id = payload.get("lead_id")
    amount = payload.get("amount", "99")
    currency = payload.get("currency", "USD")
    days = int(payload.get("days", 30))
    provider = payload.get("provider", "manual")
    payment_ref = payload.get("payment_ref")

    if not lead_id:
        raise HTTPException(status_code=400, detail="lead_id is required")

    lead = get_subscription_lead_by_id(int(lead_id))

    if not lead:
        raise HTTPException(status_code=404, detail="lead not found")

    if lead.get("status") == "cancelled":
        raise HTTPException(
            status_code=409,
            detail="cancelled lead cannot be marked as paid",
        )

    if lead.get("status") == "paid":
        raise HTTPException(
            status_code=409,
            detail="lead is already paid",
        )

    telegram_id = lead.get("telegram_user_id")
    plan = lead.get("plan") or "pro"

    if not telegram_id:
        raise HTTPException(
            status_code=400,
            detail="lead telegram_user_id is missing",
        )

    if not payment_ref:
        payment_ref = f"lead-{lead_id}-manual"

    payment_payload = {
        "telegram_id": str(telegram_id),
        "plan": plan,
        "days": days,
        "payment_ref": payment_ref,
        "provider": provider,
        "amount": amount,
        "currency": currency,
        "create_invite": True,
        "lead_id": lead_id,
        "source": "admin_lead_mark_paid",
    }

    result = admin_confirm_payment(payment_payload)

    updated_lead = mark_subscription_lead_status(int(lead_id), "paid")

    return {
        "status": "ok",
        "lead": updated_lead,
        "payment_flow": result,
    }
