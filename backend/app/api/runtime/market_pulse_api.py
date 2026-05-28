from fastapi import APIRouter, Query
from app.runtime.market_router import get_unified_market_pulse

router = APIRouter()


@router.get("/runtime/market-pulse")
async def runtime_market_pulse(
    package: str = Query("free")
):
    return get_unified_market_pulse(package)
