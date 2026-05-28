from __future__ import annotations

import os
import requests

from app.integrations.telegram.channel_router import get_channel_id


def _get_token() -> str:
    return os.getenv("TELEGRAM_BOT_TOKEN", "").strip()


def _normalize_user_id(telegram_user_id: str | int):
    try:
        return int(str(telegram_user_id).strip())
    except Exception:
        return None


def remove_member_from_channel(channel: str, telegram_user_id: str | int) -> dict:
    token = _get_token()
    chat_id = get_channel_id(channel)
    user_id = _normalize_user_id(telegram_user_id)

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

    if not user_id:
        return {
            "status": "failed",
            "reason": "telegram_user_id must be a numeric Telegram user ID",
            "telegram_user_id": str(telegram_user_id),
        }

    ban_url = f"https://api.telegram.org/bot{token}/banChatMember"
    unban_url = f"https://api.telegram.org/bot{token}/unbanChatMember"

    try:
        ban_response = requests.post(
            ban_url,
            json={
                "chat_id": chat_id,
                "user_id": user_id,
            },
            timeout=15,
        )
        ban_data = ban_response.json()

        if not ban_response.ok or not ban_data.get("ok"):
            return {
                "status": "failed",
                "step": "ban",
                "channel": channel,
                "chat_id": chat_id,
                "telegram_user_id": str(user_id),
                "status_code": ban_response.status_code,
                "body": ban_data,
            }

        unban_response = requests.post(
            unban_url,
            json={
                "chat_id": chat_id,
                "user_id": user_id,
                "only_if_banned": True,
            },
            timeout=15,
        )
        unban_data = unban_response.json()

        if not unban_response.ok or not unban_data.get("ok"):
            return {
                "status": "partial",
                "step": "unban",
                "channel": channel,
                "chat_id": chat_id,
                "telegram_user_id": str(user_id),
                "ban": ban_data,
                "status_code": unban_response.status_code,
                "body": unban_data,
            }

        return {
            "status": "ok",
            "removed": True,
            "channel": channel,
            "chat_id": chat_id,
            "telegram_user_id": str(user_id),
            "ban": ban_data,
            "unban": unban_data,
        }

    except Exception as exc:
        return {
            "status": "failed",
            "channel": channel,
            "chat_id": chat_id,
            "telegram_user_id": str(user_id),
            "error": str(exc),
        }
