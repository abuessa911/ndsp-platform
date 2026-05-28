import requests

BOT_TOKEN = "REVOKED_TOKEN_DO_NOT_USE"
CHAT_ID = "REPLACE_WITH_ENV_CHAT_ID"

def send(msg):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    try:
        requests.post(url, data=data)
    except:
        pass
