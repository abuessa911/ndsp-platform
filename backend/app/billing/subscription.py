from fastapi import HTTPException

def check_feature(user, feature):
    if feature not in user.get("plan_features", []):
        raise HTTPException(status_code=403, detail="Feature not allowed")
