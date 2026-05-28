from fastapi import APIRouter, Request
import json
from app.users_db import activate_user
from app.telegram_sender import send_signal

router = APIRouter()

@router.post("/webhook/paypal")
async def paypal_webhook(request: Request):
    data = await request.json()
    print("💰 PayPal Event:", json.dumps(data, indent=2))

    event_type = data.get("event_type")

    if event_type == "PAYMENT.SALE.COMPLETED":
        resource = data.get("resource", {})
        user_id = resource.get("custom_id")

        if user_id:
            activate_user(user_id)

            send_signal(f"✅ Subscription Activated\\nUser: {user_id}")

            print(f"🔥 User {user_id} activated")

    return {"status": "ok"}
