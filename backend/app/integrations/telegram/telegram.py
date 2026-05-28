import os
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "REVOKED_TOKEN_DO_NOT_USE"
CHAT_IDS = os.getenv("TELEGRAM_CHAT_IDS") or "-1003491841685,-1003793881886"

def send_message(text):
    if not CHAT_IDS:
        print("❌ TELEGRAM_CHAT_IDS NOT SET")
        return

    ids = CHAT_IDS.split(",")

    for chat_id in ids:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            r = requests.post(url, json={
                "chat_id": chat_id.strip(),
                "text": text,
                "parse_mode": "Markdown"
            })
            print("Telegram response:", r.text)

        except Exception as e:
            print("Telegram Error:", e)
