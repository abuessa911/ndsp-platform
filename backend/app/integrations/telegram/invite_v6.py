from __future__ import annotations

import os
import requests

from app.integrations.telegram.channel_router import get_channel_id


def _get_token() -> str:
    return os.getenv("TELEGRAM_BOT_TOKEN", "").strip()


def create_invite_link(channel: str, name: str | None = None, member_limit: int = 1) -> dict:
    token = _get_token()
    chat_id = get_channel_id(channel)

    if not token:
        return {
            "status": "not_configured",
            "reason": "TELEGRAM_BOT_TOKEN missing",
        }

    if not chat_id:
        return {
            "status": "not_configured",
            "reason": "telegram channel missing",
            "channel": channel,
        }

    url = f"https://api.telegram.org/bot{token}/createChatInviteLink"

    payload = {
        "chat_id": chat_id,
        "member_limit": member_limit,
        "creates_join_request": False,
    }

    if name:
        payload["name"] = name[:32]

    try:
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()

        if not response.ok or not data.get("ok"):
            return {
                "status": "failed",
                "channel": channel,
                "chat_id": chat_id,
                "status_code": response.status_code,
                "body": data,
            }

        return {
            "status": "ok",
            "channel": channel,
            "chat_id": chat_id,
            "invite_link": data["result"].get("invite_link"),
            "raw": data["result"],
        }

    except Exception as exc:
        return {
            "status": "failed",
            "channel": channel,
            "chat_id": chat_id,
            "error": str(exc),
        }


def revoke_invite_link(channel: str, invite_link: str) -> dict:
    token = _get_token()
    chat_id = get_channel_id(channel)

    if not token:
        return {
            "status": "not_configured",
            "reason": "TELEGRAM_BOT_TOKEN missing",
        }

    if not chat_id:
        return {
            "status": "not_configured",
            "reason": "telegram channel missing",
            "channel": channel,
        }

    if not invite_link:
        return {
            "status": "failed",
            "reason": "invite_link is required",
        }

    url = f"https://api.telegram.org/bot{token}/revokeChatInviteLink"

    try:
        response = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "invite_link": invite_link,
            },
            timeout=15,
        )
        data = response.json()

        if not response.ok or not data.get("ok"):
            return {
                "status": "failed",
                "channel": channel,
                "chat_id": chat_id,
                "status_code": response.status_code,
                "body": data,
            }

        return {
            "status": "ok",
            "channel": channel,
            "chat_id": chat_id,
            "revoked": True,
            "raw": data["result"],
        }

    except Exception as exc:
        return {
            "status": "failed",
            "channel": channel,
            "chat_id": chat_id,
            "error": str(exc),
        }


def revoke_many_invite_links(invites: list[dict]) -> list[dict]:
    results = []

    for invite in invites:
        channel = invite.get("channel")
        invite_link = invite.get("invite_link")

        if not channel or not invite_link:
            results.append({
                "status": "skipped",
                "reason": "missing channel or invite_link",
                "invite": invite,
            })
            continue

        results.append(revoke_invite_link(channel=channel, invite_link=invite_link))

    return results
