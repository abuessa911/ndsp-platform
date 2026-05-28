from fastapi import APIRouter, Request
from app.payments.core import activate_user

router = APIRouter()

@router.post("/apple")
async def apple_pay_webhook(request: Request):
    data = await request.json()

    # في الواقع Stripe يرسل event مختلف (checkout.session.completed)
    email = data.get("email", "apple@user")
    plan = data.get("plan", "pro")

    user_id = activate_user(email, plan)

    return {
        "status": "apple_pay_ok",
        "user_id": user_id
    }
