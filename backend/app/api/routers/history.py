from fastapi import APIRouter, Depends
import json

from app.core.security.api_key_auth import verify_api_key

router = APIRouter()

LOG_FILE = "/home/nawaf511/empire-core-new/backend/logs/decisions.log"


@router.get("/history")
def get_history(user: dict = Depends(verify_api_key)):

    results = []

    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                entry = json.loads(line)

                if entry.get("user_id") == user["id"]:
                    results.append(entry)

    except Exception as e:
        return {"error": str(e)}

    return {
        "count": len(results),
        "data": results[-50:]
    }
