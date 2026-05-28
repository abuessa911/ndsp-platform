from __future__ import annotations

from app.core.delivery.ndsp_env_compat import telegram_token, telegram_chat_ids, telegram_chat_id

import os
from typing import List
import requests

from app.integrations.telegram.channel_router import get_channel_id

def _get_token() -> str:
    return telegram_token()

def _split_chat_ids(raw: str) -> List[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]

def _get_default_chat_ids() -> List[str]:
    raw = telegram_chat_ids()
    if raw:
        return _split_chat_ids(raw)

    single = telegram_chat_id()
    return [single] if single else []

def _get_target_chat_ids(channel: str | None = None) -> List[str]:
    if channel:
        channel_id = get_channel_id(channel)
        return [channel_id] if channel_id else []

    return _get_default_chat_ids()

def telegram_status() -> dict:
    token = _get_token()
    default_chat_ids = _get_default_chat_ids()

    return {
        "configured": bool(token and default_chat_ids),
        "has_token": bool(token),
        "default_chat_ids_count": len(default_chat_ids),
        "pro_channel": bool(get_channel_id("pro")),
        "vip_channel": bool(get_channel_id("vip")),
    }

def send_telegram_message(text: str, channel: str | None = None) -> dict:
    token = _get_token()
    chat_ids = _get_target_chat_ids(channel)

    if not token:
        return {"status": "not_configured", "reason": "TELEGRAM_BOT_TOKEN missing"}

    if not chat_ids:
        return {
            "status": "not_configured",
            "reason": "telegram target channel missing",
            "channel": channel,
        }

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    results = []

    for chat_id in chat_ids:
        try:
            response = requests.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                },
                timeout=15,
            )
            results.append({
                "chat_id": chat_id,
                "status_code": response.status_code,
                "ok": response.ok,
                "body": response.text[:500],
            })
        except Exception as exc:
            results.append({
                "chat_id": chat_id,
                "ok": False,
                "error": str(exc),
            })

    success = any(item.get("ok") for item in results)

    return {
        "status": "sent" if success else "failed",
        "channel": channel,
        "results": results,
    }
