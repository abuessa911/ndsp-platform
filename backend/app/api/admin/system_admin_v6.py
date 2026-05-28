from __future__ import annotations

from fastapi import APIRouter, Depends

from app.governance.admin_only import require_admin_role
from app.saas.subscriptions_db import (
    list_subscriptions,
    list_invites,
    list_payments,
    list_telegram_users,
    list_subscription_leads,
)
from app.integrations.telegram.unified_sender import telegram_status

router = APIRouter(prefix="/api/admin/system", tags=["system-admin"])


def _count_by(items: list[dict], key: str) -> dict:
    result = {}
    for item in items:
        value = item.get(key) or "unknown"
        result[value] = result.get(value, 0) + 1
    return result


@router.get("/status", dependencies=[Depends(require_admin_role)])
def admin_system_status():
    subscriptions = list_subscriptions()
    invites = list_invites()
    payments = list_payments()
    telegram_users = list_telegram_users()
    leads = list_subscription_leads()

    active_subscriptions = [
        item for item in subscriptions
        if item.get("status") == "active"
    ]

    cancelled_subscriptions = [
        item for item in subscriptions
        if item.get("status") == "cancelled"
    ]

    active_invites = [
        item for item in invites
        if item.get("status") == "active"
    ]

    revoked_invites = [
        item for item in invites
        if item.get("status") == "revoked"
    ]

    return {
        "status": "ok",
        "api": {
            "state": "running",
            "version": "v6",
        },
        "telegram": telegram_status(),
        "subscriptions": {
            "total": len(subscriptions),
            "active": len(active_subscriptions),
            "cancelled": len(cancelled_subscriptions),
            "by_plan": _count_by(subscriptions, "plan"),
            "by_status": _count_by(subscriptions, "status"),
            "latest": subscriptions[:5],
        },
        "payments": {
            "total": len(payments),
            "by_provider": _count_by(payments, "provider"),
            "by_status": _count_by(payments, "status"),
            "latest": payments[:5],
        },
        "invites": {
            "total": len(invites),
            "active": len(active_invites),
            "revoked": len(revoked_invites),
            "by_channel": _count_by(invites, "channel"),
            "by_status": _count_by(invites, "status"),
            "latest": invites[:5],
        },
        "telegram_users": {
            "total": len(telegram_users),
            "latest": telegram_users[:5],
        },
        "leads": {
            "total": len(leads),
            "by_plan": _count_by(leads, "plan"),
            "by_status": _count_by(leads, "status"),
            "latest": leads[:5],
        },
    }
