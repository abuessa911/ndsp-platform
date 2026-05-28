from fastapi import APIRouter
from app.engine.subscription_db import add_user
import paypalrestsdk
import requests

router = APIRouter()

# ========================
# 💳 PAYPAL
# ========================

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_SECRET"
})


@router.get("/pay/paypal/{chat_id}")
def paypal_payment(chat_id: str):

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": f"https://api.ndsp.app/pay/success/{chat_id}",
            "cancel_url": "https://t.me/YOUR_BOT"
        },
        "transactions": [{
            "amount": {"total": "15.00", "currency": "USD"},
            "description": "VIP 30 Days"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return {"url": link.href}

    return {"error": "paypal failed"}


@router.get("/pay/success/{chat_id}")
def paypal_success(chat_id: str):

    add_user(chat_id)

    return {"status": "activated"}


# ========================
# 🪙 USDT (TRC20)
# ========================

USDT_ADDRESS = "YOUR_WALLET_ADDRESS"

# 🔥 إنشاء طلب دفع
@router.get("/pay/usdt/{chat_id}")
def usdt_payment(chat_id: str):

    return {
        "address": USDT_ADDRESS,
        "amount": 15,
        "network": "TRC20",
        "note": f"Send EXACT amount then contact admin with TXID: {chat_id}"
    }


# ========================
# 🔍 تحقق USDT (اختياري)
# ========================

def check_usdt_payment(txid):

    url = f"https://apilist.tronscanapi.com/api/transaction-info?hash={txid}"
    res = requests.get(url).json()

    if "contractData" in res:
        return True

    return False
