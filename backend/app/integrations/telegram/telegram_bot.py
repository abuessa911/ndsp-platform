import requests

TOKEN = "REVOKED_TOKEN_DO_NOT_USE"
CHAT_ID = "REPLACE_WITH_ENV_CHAT_ID"

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg
    })
