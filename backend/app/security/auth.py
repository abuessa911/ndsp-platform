from fastapi import Header, HTTPException, Depends

# 🔥 API Keys Database (مؤقت - لاحقًا DB)
API_KEYS = {
    "admin_key_123": {"role": "admin", "plan": "institutional"},
    "pro_key_123": {"role": "user", "plan": "pro"},
    "free_key_123": {"role": "user", "plan": "free"},
}

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return API_KEYS[x_api_key]

def require_role(required_role: str):
    def role_checker(user=Depends(verify_api_key)):
        if user["role"] != required_role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_checker
