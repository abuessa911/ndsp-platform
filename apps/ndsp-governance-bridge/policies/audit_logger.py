import json
from datetime import datetime

LOG_FILE = "/home/nawaf511/empire-core-new/backend/logs/decisions.log"

def log_decision(data: dict, user: dict = None):

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user.get("id") if user else None,
        "plan": user.get("plan") if user else None,
        "data": data
    }

    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print("AUDIT LOG ERROR:", e)
