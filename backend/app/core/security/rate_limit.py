import json
import os
from datetime import datetime
from fastapi import HTTPException

USAGE_FILE = "/home/nawaf511/empire-core-new/backend/data/usage.json"

PLAN_LIMITS = {
    "free": 20,
    "pro": 1000,
    "vip": 999999
}

def load_usage():
    if not os.path.exists(USAGE_FILE):
        return []

    with open(USAGE_FILE, "r") as f:
        return json.load(f)

def save_usage(data):
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_today():
    return datetime.utcnow().strftime("%Y-%m-%d")

def check_and_update_usage(user_id, plan):
    usage = load_usage()
    today = get_today()

    limit = PLAN_LIMITS.get(plan, 10)

    for u in usage:
        if u["user_id"] == user_id:

            # 🔄 يوم جديد → تصفير
            if u["date"] != today:
                u["date"] = today
                u["count"] = 0

            # ❌ تجاوز الحد
            if u["count"] >= limit:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded ({limit}/day)"
                )

            # ➕ زيادة
            u["count"] += 1
            save_usage(usage)

            return {
                "used": u["count"],
                "limit": limit,
                "remaining": limit - u["count"]
            }

    # 🆕 مستخدم جديد
    new_user = {
        "user_id": user_id,
        "date": today,
        "count": 1
    }

    usage.append(new_user)
    save_usage(usage)

    return {
        "used": 1,
        "limit": limit,
        "remaining": limit - 1
    }
