from fastapi import Depends
from app.security.auth import verify_api_key
from app.security.rate_limit import rate_limiter
from app.billing.plans import PLANS

def get_current_user(user=Depends(verify_api_key)):
    plan = user["plan"]
    user["plan_features"] = PLANS[plan]["features"]
    return user

def enforce_rate_limit(user=Depends(get_current_user)):
    rate_limiter(user["plan"])
    return user
