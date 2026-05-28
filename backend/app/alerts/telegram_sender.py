from __future__ import annotations

import os
import requests

from app.integrations.telegram.unified_sender import send_telegram_message


def send_telegram(message: str):
    return send_telegram_message(message)


def send_telegram_to_chat(chat_id: str, message: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

    if not token:
        return {
            "status": "not_configured",
            "reason": "TELEGRAM_BOT_TOKEN missing",
        }

    if not chat_id:
        return {
            "status": "failed",
            "reason": "chat_id missing",
        }

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": str(chat_id),
        "text": message,
        "disable_web_page_preview": True,
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        try:
            body = response.json()
        except Exception:
            body = response.text

        return {
            "status": "sent" if response.ok else "failed",
            "chat_id": str(chat_id),
            "status_code": response.status_code,
            "ok": response.ok,
            "body": body,
        }
    except Exception as exc:
        return {
            "status": "failed",
            "reason": str(exc),
            "chat_id": str(chat_id),
        }
