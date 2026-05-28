from fastapi import APIRouter
from datetime import datetime

from app.engine.subscription_db import get_all_users
from app.engine.referral_system import load as load_ref
from app.engine.user_tracking import load as load_tracking
from app.engine.ai_security import evaluate_user

router = APIRouter()


@router.get("/admin/dashboard")
def dashboard():

    subs = get_all_users()
    refs = load_ref()
    tracking = load_tracking()

    result = []

    for user_id, data in subs.items():

        expire = data["expires"]
        expire_date = datetime.fromisoformat(expire)

        status = "ACTIVE" if datetime.utcnow() < expire_date else "EXPIRED"

        # 💰 أرباح
        earnings = 0
        users = 0

        if user_id in refs:
            earnings = refs[user_id]["earnings"]
            users = len(refs[user_id]["users"])

        # 🧠 AI
        ai_status = evaluate_user(user_id)

        result.append({
            "user_id": user_id,
            "status": status,
            "ai": ai_status,
            "ref_users": users,
            "earnings": earnings
        })

    return result
