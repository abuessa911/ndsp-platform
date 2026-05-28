from __future__ import annotations

import json

from fastapi import APIRouter, Depends, Body, HTTPException

from app.governance.admin_only import require_admin_role
from app.saas.subscriptions_db import (
    upsert_subscription,
    is_active_subscription,
    save_invite,
    save_payment,
    list_payments,
    get_payment_by_ref,
    mark_active_invites_revoked_for_other_channels,
    save_audit_event,
)
from app.saas.plans import get_plan, get_plan_channel
from app.integrations.telegram.invite_v6 import create_invite_link, revoke_many_invite_links
from app.alerts.telegram_sender import send_telegram_to_chat
from app.core.elite_trial_capacity import enforce_elite_trial_capacity
router = APIRouter(prefix="/api/admin/payments", tags=["payments-admin"])


@router.get("", dependencies=[Depends(require_admin_role)])
def admin_list_payments():
    return {
        "status": "ok",
        "payments": list_payments(),
    }


@router.post("/confirm", dependencies=[Depends(require_admin_role)])
def admin_confirm_payment(payload: dict = Body(default={})):
    email = payload.get("email")
    telegram_id = payload.get("telegram_id")
    plan = payload.get("plan", "pro")
    days = int(payload.get("days", 30))
    payment_ref = payload.get("payment_ref", "manual")
    provider = payload.get("provider", "manual")
    amount = payload.get("amount")
    currency = payload.get("currency")
    create_invite = bool(payload.get("create_invite", True))

    if not email and not telegram_id:
        raise HTTPException(status_code=400, detail="email or telegram_id is required")

    existing_payment = get_payment_by_ref(provider=provider, payment_ref=payment_ref)

    if existing_payment:
        save_audit_event(
            event_type="payment_duplicate",
            entity_type="payment",
            entity_id=str(existing_payment.get("id")),
            actor_type="webhook" if provider != "manual" else "admin",
            actor_id=str(telegram_id or email or ""),
            message="Duplicate payment_ref ignored",
            payload_json=json.dumps({
                "provider": provider,
                "payment_ref": payment_ref,
                "telegram_id": telegram_id,
                "email": email,
                "event_type": "payment_duplicate"
            }, ensure_ascii=False),
        )

        return {
            "status": "ok",
            "already_processed": True,
            "payment": existing_payment,
            "subscription": None,
            "active": None,
            "plan_features": get_plan(plan),
            "invite": None,
            "saved_invite": None,
            "invite_delivery": {
                "status": "skipped",
                "reason": "payment_ref already processed",
            },
            "revoked_old_invites": [],
            "revoke_results": [],
        }

    plan_info = get_plan(plan)

    sub = upsert_subscription(
        email=email,
        telegram_id=telegram_id,
        plan=plan,
        status="active",
        days=days,
    )

    payment = save_payment(
        payment_ref=payment_ref,
        provider=provider,
        email=email,
        telegram_id=telegram_id,
        plan=plan,
        amount=str(amount) if amount is not None else None,
        currency=currency,
        status="confirmed",
        subscription_id=sub.get("id"),
        raw=json.dumps(payload, ensure_ascii=False),
    )

    save_audit_event(
        event_type="payment_confirmed",
        entity_type="payment",
        entity_id=str(payment.get("id")),
        actor_type="webhook" if provider != "manual" else "admin",
        actor_id=str(telegram_id or email or ""),
        message="Payment confirmed and saved",
        payload_json=json.dumps(payment, ensure_ascii=False),
    )

    save_audit_event(
        event_type="subscription_activated",
        entity_type="subscription",
        entity_id=str(sub.get("id")),
        actor_type="system",
        actor_id=str(telegram_id or email or ""),
        message="Subscription activated from confirmed payment",
        payload_json=json.dumps(sub, ensure_ascii=False),
    )

    invite = None
    saved_invite = None
    invite_delivery = None
    revoked_old_invites = []
    revoke_results = []

    channel = get_plan_channel(plan)

    if channel:
        revoked_old_invites = mark_active_invites_revoked_for_other_channels(
            subscription_id=sub["id"],
            keep_channel=channel,
        )
        revoke_results = revoke_many_invite_links(revoked_old_invites)

    if create_invite and channel:
        label = f"NDSP-{plan}-{sub.get('id')}-{payment_ref}"
        invite = create_invite_link(channel=channel, name=label, member_limit=1)

        if invite.get("status") == "ok" and invite.get("invite_link"):
            saved_invite = save_invite(
                subscription_id=sub["id"],
                channel=channel,
                invite_link=invite["invite_link"],
                raw=json.dumps(invite.get("raw", {}), ensure_ascii=False),
            )

            save_audit_event(
                event_type="invite_created",
                entity_type="subscription_invite",
                entity_id=str(saved_invite.get("id") if saved_invite else ""),
                actor_type="system",
                actor_id=str(telegram_id or ""),
                message="Telegram invite created",
                payload_json=json.dumps(saved_invite, ensure_ascii=False),
            )

            if telegram_id:
                try:
                    invite_message = "\n".join(
                        [
                            "✅ NDSP subscription activated.",
                            "",
                            f"Plan: {plan}",
                            "",
                            "Your private access link:",
                            invite["invite_link"],
                            "",
                            "This link is private, single-use, and time-limited.",
                        ]
                    )

                    send_telegram_to_chat(
                        str(telegram_id),
                        invite_message,
                    )

                    invite_delivery = {
                        "status": "sent",
                        "telegram_id": str(telegram_id),
                    }

                    save_audit_event(
                        event_type="invite_sent",
                        entity_type="telegram_user",
                        entity_id=str(telegram_id),
                        actor_type="system",
                        actor_id=str(telegram_id),
                        message="Telegram invite delivered to user",
                        payload_json=json.dumps(invite_delivery, ensure_ascii=False),
                    )

                except Exception as exc:
                    invite_delivery = {
                        "status": "failed",
                        "telegram_id": str(telegram_id),
                        "error": str(exc),
                    }

                    save_audit_event(
                        event_type="invite_delivery_failed",
                        entity_type="telegram_user",
                        entity_id=str(telegram_id),
                        actor_type="system",
                        actor_id=str(telegram_id),
                        message="Telegram invite delivery failed",
                        payload_json=json.dumps(invite_delivery, ensure_ascii=False),
                    )

    return {
        "status": "ok",
        "payment": payment,
        "subscription": sub,
        "active": is_active_subscription(sub),
        "plan_features": plan_info,
        "invite": invite,
        "saved_invite": saved_invite,
        "invite_delivery": invite_delivery,
        "revoked_old_invites": revoked_old_invites,
        "revoke_results": revoke_results,
    }


@router.post("/manual-pro", dependencies=[Depends(require_admin_role)])
def admin_manual_pro(payload: dict = Body(default={})):
    payload["plan"] = "pro"
    payload.setdefault("days", 30)
    payload.setdefault("payment_ref", "manual-pro")
    payload.setdefault("provider", "manual")
    return admin_confirm_payment(payload)


@router.post("/manual-elite", dependencies=[Depends(require_admin_role)])
def admin_manual_elite(payload: dict = Body(default={})):
    payload["plan"] = "elite"
    payload.setdefault("days", 30)
    payload.setdefault("payment_ref", "manual-elite")
    payload.setdefault("provider", "manual")
    return admin_confirm_payment(payload)
