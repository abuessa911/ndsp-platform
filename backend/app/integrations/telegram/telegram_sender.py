import requests

BOT_TOKEN = "REVOKED_TOKEN_DO_NOT_USE"
CHAT_ID = "302572192"

def send_signal(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    r = requests.post(url, json=payload)
    print("Telegram Response:", r.text)
    return r.json()
