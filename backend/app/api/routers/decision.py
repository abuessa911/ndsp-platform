from fastapi import APIRouter, Query, Depends

from app.core.governed_pipeline import run_governed
from app.core.security.api_key_auth import verify_api_key
from app.core.security.rate_limit import check_and_update_usage

router = APIRouter()


@router.get("/decision")
def get_decision(
    symbol: str = Query(...),
    user: dict = Depends(verify_api_key),
):
    """
    NDSP Governance v6 decision endpoint.

    Backend = Brain
    UI = Interface

    Returns governed Contract v1.0.0 only.
    No client-side decision logic.
    No BUY/SELL/TP/SL output.
    """

    usage = check_and_update_usage(user["id"], user["plan"])

    result = run_governed(symbol)

    result["meta"] = result.get("meta", {})
    result["meta"]["user_id"] = user["id"]
    result["meta"]["plan"] = user["plan"]
    result["meta"]["usage"] = usage

    return result
