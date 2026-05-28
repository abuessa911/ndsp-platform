# /opt/empire-core/backend/app/integrations/telegram/invite_manager.py

import requests
import os

from app.integrations.telegram.channels import CHANNELS

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


def create_invite_link(plan: str) -> str:

    channel_id = CHANNELS.get(plan)

    if not channel_id:
        print("❌ No channel for plan:", plan)
        return None

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/createChatInviteLink"

    payload = {
        "chat_id": channel_id,
        "member_limit": 1  # 🔥 رابط استخدام واحد فقط
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        data = response.json()

        if data.get("ok"):
            return data["result"]["invite_link"]
        else:
            print("❌ Telegram API error:", data)

    except Exception as e:
        print("❌ Error:", e)

    return None
