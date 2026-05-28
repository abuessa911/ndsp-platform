from fastapi import APIRouter, Request
from app.services.payment_service import confirm_payment

router = APIRouter()

########################################
# 🚀 MOYASAR WEBHOOK
########################################
@router.post("/webhook/moyasar")
async def moyasar_webhook(request: Request):

    data = await request.json()

    # 💀 تحقق من الدفع
    status = data.get("status")
    metadata = data.get("metadata", {})

    payment_id = metadata.get("payment_id")

    if status == "paid" and payment_id:
        result = confirm_payment(payment_id)

        return {
            "status": "confirmed",
            "api_key": result.get("api_key")
        }

    return {"status": "ignored"}
