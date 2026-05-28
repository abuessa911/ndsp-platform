from fastapi import APIRouter
import json
import os

router = APIRouter()

USERS_DB = "/home/nawaf511/empire-core-new/backend/data/users.json"
SIGNALS_LOG = "/home/nawaf511/empire-core-new/backend/logs/signals.log"

def get_users_count():
    if not os.path.exists(USERS_DB):
        return 0
    with open(USERS_DB) as f:
        data = json.load(f)
        return len(data)

def get_revenue():
    users = get_users_count()
    return users * 50  # سعر الاشتراك

def get_signals_count():
    if not os.path.exists(SIGNALS_LOG):
        return 0
    with open(SIGNALS_LOG) as f:
        return len(f.readlines())

@router.get("/dashboard")
def dashboard():
    return {
        "users": get_users_count(),
        "revenue": get_revenue(),
        "signals": get_signals_count(),
        "status": "Empire Running 🔥"
    }
