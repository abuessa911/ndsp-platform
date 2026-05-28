from fastapi import APIRouter, Request
import paypalrestsdk
import requests

from app.engine.subscription_db import add_user
from app.engine.config import TELEGRAM_BOT_TOKEN

router = APIRouter()


# =========================
# 💰 إنشاء الدفع
# =========================
@router.post("/paypal/create")
async def create_payment(req: Request):

    data = await req.json()
    chat_id = data.get("chat_id")

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "https://api.ndsp.app/success",
            "cancel_url": "https://api.ndsp.app/cancel"
        },
        "transactions": [{
            "amount": {
                "total": "10.00",
                "currency": "USD"
            },
            "description": "VIP 30 Days",

            # 🔥 الربط
            "custom": str(chat_id)
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return {"url": link.href}

    return {"error": "failed"}


# =========================
# 🔥 Webhook PayPal
# =========================
@router.post("/paypal/webhook")
async def paypal_webhook(req: Request):

    data = await req.json()
    print("💰 PAYPAL:", data)

    try:
        chat_id = int(
            data["resource"]["transactions"][0]["custom"]
        )

        add_user(chat_id)

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": "🎉 تم تفعيل اشتراكك بنجاح!\n💎 يمكنك الآن دخول VIP"
            }
        )

    except Exception as e:
        print("🔥 PAYPAL ERROR:", e)

    return {"ok": True}
