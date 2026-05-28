from fastapi import APIRouter
from datetime import datetime
from app.engine.subscription_db import get_all_users, remove_user
from app.engine.telegram_admin import kick_user

router = APIRouter()

@router.get("/admin/subscriptions")
def get_subscriptions():

    db = get_all_users()
    now = datetime.utcnow()

    result = []

    for user_id, data in db.items():
        expire_date = datetime.fromisoformat(data["expires"])

        status = "ACTIVE" if now < expire_date else "EXPIRED"

        result.append({
            "user_id": user_id,
            "expires": data["expires"],
            "status": status
        })

    return result


@router.delete("/admin/remove/{user_id}")
def remove_subscription(user_id: str):

    kick_user(user_id)
    remove_user(user_id)

    return {"status": "removed"}
