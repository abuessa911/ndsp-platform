from fastapi import APIRouter, Query, Depends

# استبدال المنسق القديم بمنسق V4.1
from app.core.ndsp_v4_pipeline import run_ndsp_v4_pipeline
from app.core.security.api_key_auth import verify_api_key
from app.core.security.rate_limit import check_and_update_usage

router = APIRouter()

@router.get("/decision")
def get_decision(
    symbol: str = Query(...),
    user: dict = Depends(verify_api_key)
):
    """
    NDSP Governance V4.1 Decision Endpoint.
    Returns governed Contract V4.1 only.
    """

    ########################################
    # 💀 RATE LIMIT
    ########################################
    usage = check_and_update_usage(user["id"], user["plan"])

    ########################################
    # 💀 NDSP GOVERNED PIPELINE V4.1
    ########################################
    result = run_ndsp_v4_pipeline(symbol)

    ########################################
    # 💀 RESPONSE FORMATTING
    ########################################
    result["meta"] = {
        "user_id": user["id"],
        "plan": user["plan"],
        "usage": usage,
        "architecture": "NDSP Decision Architecture V4.1"
    }

    return {
        "status": "ok",
        "data": result
    }
