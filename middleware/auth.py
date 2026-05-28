from fastapi import Header, HTTPException
from app.services.auth_service import get_user_by_key

def verify_user(x_api_key: str = Header(...)):
    user = get_user_by_key(x_api_key)

    if not user:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    return user
