from fastapi import APIRouter, Request
from app.services.payment_store import update_payment_status
from app.services.api_keys import generate_api_key

router = APIRouter()

@router.post("/webhook/crypto")
async def crypto_webhook(request: Request):

    data = await request.json()

    print("💀 WEBHOOK DATA:", data)

    payment_id = data.get("order_id")
    status = data.get("payment_status")

    if not payment_id:
        return {"status": False, "error": "missing_order_id"}

    ########################################
    # 💀 حالة الدفع
    ########################################
    if status in ["finished", "confirmed"]:

        # 💾 تحديث الدفع
        payment = update_payment_status(payment_id, "paid")

        if not payment:
            return {"status": False, "error": "payment_not_found"}

        ########################################
        # 🔑 إنشاء API KEY
        ########################################
        api_key = generate_api_key(payment["plan"])

        print("💀 ACTIVATED:", api_key)

        return {
            "status": True,
            "message": "payment confirmed",
            "api_key": api_key
        }

    return {"status": True, "message": "ignored"}
