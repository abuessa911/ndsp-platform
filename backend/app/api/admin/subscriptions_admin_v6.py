from __future__ import annotations

import json

from fastapi import APIRouter, Depends, Body, Query, HTTPException

from app.governance.admin_only import require_admin_role
from app.integrations.telegram.invite_v6 import (
    create_invite_link,
    revoke_invite_link,
    revoke_many_invite_links,
)
from app.integrations.telegram.member_v6 import remove_member_from_channel
from app.saas.plans import get_plan, get_plan_channel
from app.saas.subscriptions_db import (
    init_db,
    init_invites_table,
    upsert_subscription,
    get_subscription,
    list_subscriptions,
    cancel_subscription,
    is_active_subscription,
    save_invite,
    list_invites,
    mark_invite_revoked,
    mark_active_invites_revoked_for_other_channels,
)

router = APIRouter(prefix="/api/admin/subscriptions", tags=["subscriptions-admin"])


@router.on_event("startup")
def startup():
    init_db()
    init_invites_table()


@router.get("", dependencies=[Depends(require_admin_role)])
def admin_list_subscriptions():
    return {
        "status": "ok",
        "subscriptions": list_subscriptions(),
    }


@router.post("/upsert", dependencies=[Depends(require_admin_role)])
def admin_upsert_subscription(payload: dict = Body(default={})):
    email = payload.get("email")
    telegram_id = payload.get("telegram_id")
    plan = payload.get("plan", "free")
    status = payload.get("status", "active")
    days = int(payload.get("days", 30))

    plan_info = get_plan(plan)

    sub = upsert_subscription(
        email=email,
        telegram_id=telegram_id,
        plan=plan,
        status=status,
        days=days,
    )

    return {
        "status": "ok",
        "subscription": sub,
        "plan_features": plan_info,
    }


@router.get("/lookup", dependencies=[Depends(require_admin_role)])
def admin_lookup_subscription(
    email: str | None = Query(default=None),
    telegram_id: str | None = Query(default=None),
):
    sub = get_subscription(email=email, telegram_id=telegram_id)

    return {
        "status": "ok",
        "active": is_active_subscription(sub),
        "subscription": sub,
        "plan_features": get_plan(sub.get("plan")) if sub else get_plan("guest"),
        "invites": list_invites(sub["id"]) if sub else [],
    }


@router.post("/cancel", dependencies=[Depends(require_admin_role)])
def admin_cancel_subscription(payload: dict = Body(default={})):
    email = payload.get("email")
    telegram_id = payload.get("telegram_id")
    telegram_user_id = payload.get("telegram_user_id") or telegram_id
    remove_member = bool(payload.get("remove_member", True))

    existing = get_subscription(email=email, telegram_id=telegram_id)
    if not existing:
        raise HTTPException(status_code=404, detail="subscription not found")

    channel = get_plan_channel(existing.get("plan"))
    removal_result = None

    if remove_member and channel and telegram_user_id:
        removal_result = remove_member_from_channel(
            channel=channel,
            telegram_user_id=telegram_user_id,
        )

    sub = cancel_subscription(email=email, telegram_id=telegram_id)

    return {
        "status": "ok",
        "subscription": sub,
        "channel": channel,
        "removal": removal_result,
    }


@router.post("/invite", dependencies=[Depends(require_admin_role)])
def admin_create_subscription_invite(payload: dict = Body(default={})):
    email = payload.get("email")
    telegram_id = payload.get("telegram_id")

    sub = get_subscription(email=email, telegram_id=telegram_id)
    if not sub:
        raise HTTPException(status_code=404, detail="subscription not found")

    if not is_active_subscription(sub):
        raise HTTPException(status_code=403, detail="subscription is not active")

    channel = get_plan_channel(sub.get("plan"))
    if not channel:
        raise HTTPException(status_code=403, detail="plan has no telegram channel")

    revoked_old_invites = mark_active_invites_revoked_for_other_channels(
        subscription_id=sub["id"],
        keep_channel=channel,
    )
    revoke_results = revoke_many_invite_links(revoked_old_invites)

    label = f"NDSP-{sub.get('plan')}-{sub.get('id')}"
    invite = create_invite_link(channel=channel, name=label, member_limit=1)

    saved = None
    if invite.get("status") == "ok" and invite.get("invite_link"):
        saved = save_invite(
            subscription_id=sub["id"],
            channel=channel,
            invite_link=invite["invite_link"],
            raw=json.dumps(invite.get("raw", {}), ensure_ascii=False),
        )

    return {
        "status": "ok" if invite.get("status") == "ok" else "failed",
        "subscription": sub,
        "channel": channel,
        "invite": invite,
        "saved_invite": saved,
        "revoked_old_invites": revoked_old_invites,
        "revoke_results": revoke_results,
    }


@router.get("/invites", dependencies=[Depends(require_admin_role)])
def admin_list_invites(
    subscription_id: int | None = Query(default=None),
):
    return {
        "status": "ok",
        "invites": list_invites(subscription_id=subscription_id),
    }


@router.post("/revoke-invite", dependencies=[Depends(require_admin_role)])
def admin_revoke_subscription_invite(payload: dict = Body(default={})):
    channel = payload.get("channel")
    invite_link = payload.get("invite_link")

    if not channel:
        raise HTTPException(status_code=400, detail="channel is required")

    if not invite_link:
        raise HTTPException(status_code=400, detail="invite_link is required")

    result = revoke_invite_link(channel=channel, invite_link=invite_link)
    db_record = None

    if result.get("status") == "ok":
        db_record = mark_invite_revoked(invite_link)

    return {
        "status": "ok" if result.get("status") == "ok" else "failed",
        "channel": channel,
        "result": result,
        "db_record": db_record,
    }


@router.post("/remove-member", dependencies=[Depends(require_admin_role)])
def admin_remove_subscription_member(payload: dict = Body(default={})):
    email = payload.get("email")
    telegram_id = payload.get("telegram_id")
    telegram_user_id = payload.get("telegram_user_id") or telegram_id

    sub = get_subscription(email=email, telegram_id=telegram_id)
    if not sub:
        raise HTTPException(status_code=404, detail="subscription not found")

    channel = get_plan_channel(sub.get("plan"))
    if not channel:
        raise HTTPException(status_code=403, detail="plan has no telegram channel")

    if not telegram_user_id:
        raise HTTPException(status_code=400, detail="telegram_user_id is required")

    result = remove_member_from_channel(
        channel=channel,
        telegram_user_id=telegram_user_id,
    )

    return {
        "status": "ok" if result.get("status") in ("ok", "partial") else "failed",
        "subscription": sub,
        "channel": channel,
        "result": result,
    }


@router.post("/enforce-plan-channel", dependencies=[Depends(require_admin_role)])
def admin_enforce_subscription_plan_channel(payload: dict = Body(default={})):
    email = payload.get("email")
    telegram_id = payload.get("telegram_id")

    sub = get_subscription(email=email, telegram_id=telegram_id)
    if not sub:
        raise HTTPException(status_code=404, detail="subscription not found")

    channel = get_plan_channel(sub.get("plan"))
    if not channel:
        raise HTTPException(status_code=403, detail="plan has no telegram channel")

    revoked = mark_active_invites_revoked_for_other_channels(
        subscription_id=sub["id"],
        keep_channel=channel,
    )
    revoke_results = revoke_many_invite_links(revoked)

    return {
        "status": "ok",
        "subscription": sub,
        "keep_channel": channel,
        "revoked_old_invites": revoked,
        "revoke_results": revoke_results,
    }


@router.post("/cleanup-test", dependencies=[Depends(require_admin_role)])
def admin_cleanup_test_subscription(payload: dict = Body(default={})):
    email = payload.get("email")
    telegram_id = payload.get("telegram_id")

    sub = get_subscription(email=email, telegram_id=telegram_id)
    if not sub:
        raise HTTPException(status_code=404, detail="subscription not found")

    invites = list_invites(subscription_id=sub["id"])
    active_invites = [item for item in invites if item.get("status") == "active"]

    revoke_results = revoke_many_invite_links(active_invites)

    for item in active_invites:
        invite_link = item.get("invite_link")
        if invite_link:
            mark_invite_revoked(invite_link)

    cancelled = cancel_subscription(
        email=sub.get("email"),
        telegram_id=sub.get("telegram_id"),
    )

    return {
        "status": "ok",
        "subscription_before": sub,
        "subscription_after": cancelled,
        "revoked_invites": active_invites,
        "revoke_results": revoke_results,
    }
