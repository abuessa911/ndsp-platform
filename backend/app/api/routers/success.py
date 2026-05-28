from fastapi import APIRouter, Query
from app.services.payment_service import PAYMENTS_DB

router = APIRouter()

@router.get("/payment/success")
def success(payment_id: str = Query(...)):

    payment = PAYMENTS_DB.get(payment_id)

    if not payment:
        return {"error": "payment_not_found"}

    if payment.get("status") != "paid":
        return {"status": "pending"}

    return {
        "status": "success",
        "plan": payment.get("plan"),
        "api_key": payment.get("api_key")
    }
