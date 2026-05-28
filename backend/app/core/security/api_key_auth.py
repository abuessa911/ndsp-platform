from fastapi import Header, HTTPException
import json
import os
from datetime import datetime

API_KEYS_FILE = "/home/nawaf511/empire-core-new/backend/data/api_keys.json"

def load_keys():
    if not os.path.exists(API_KEYS_FILE):
        return []

    with open(API_KEYS_FILE, "r") as f:
        return json.load(f)

def verify_api_key(x_api_key: str = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")

    keys = load_keys()

    for k in keys:
        if k.get("key") == x_api_key:

            # 🔥 تحقق من الانتهاء
            expires_at = k.get("expires_at")
            if expires_at:
                if datetime.fromisoformat(expires_at) < datetime.utcnow():
                    raise HTTPException(status_code=403, detail="API key expired")

            return {
                "id": "user_" + x_api_key[:6],
                "plan": k.get("plan", "free")
            }

    raise HTTPException(status_code=403, detail="Invalid API key")
