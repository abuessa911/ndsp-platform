from fastapi import APIRouter
from pydantic import BaseModel
from app.services.payment_service import create_payment
from app.services.moyasar_service import create_moyasar_payment
from app.services.crypto_service import get_crypto_address

router = APIRouter()

########################################
# 💀 REQUEST MODEL
########################################
class PaymentRequest(BaseModel):
    plan: str
    method: str

########################################
# 🚀 CREATE PAYMENT
########################################
@router.post("/payment/create")
def create(req: PaymentRequest):

    payment = create_payment(req.plan, req.method)

    if req.method == "moyasar":
        moyasar = create_moyasar_payment(
            amount=7500 if req.plan == "pro" else 15000,
            description=req.plan,
            payment_id=payment["id"]
        )
        return {
            "payment_id": payment["id"],
            "gateway": moyasar
        }

    if req.method == "crypto":
        crypto = get_crypto_address(req.plan)
        return {
            "payment_id": payment["id"],
            "crypto": crypto
        }

    return {"error": "invalid_method"}
