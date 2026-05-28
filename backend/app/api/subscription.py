from fastapi import APIRouter
from app.engine.subscription_config import VIP_INVITE_LINK

router = APIRouter()

@router.get("/subscribe")
def subscribe():
    return {
        "status": "success",
        "message": "🎉 تم تفعيل الاشتراك",
        "vip_link": VIP_INVITE_LINK
    }
