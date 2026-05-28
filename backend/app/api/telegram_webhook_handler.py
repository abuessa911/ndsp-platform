from fastapi import APIRouter, Request
import requests
import threading

router = APIRouter()

BOT_TOKEN = "REVOKED_TOKEN_DO_NOT_USE"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("📩", data)

    msg = data.get("message")
    if not msg:
        return {"ok": True}

    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")

    def process():
        if text == "/status":
            send_message(chat_id, "🔥 Empire LIVE")
        else:
            send_message(chat_id, "جاهز")

    threading.Thread(target=process).start()

    return {"ok": True}
