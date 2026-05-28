from fastapi import APIRouter, Query

from app.services.signal_service import build_signal
from app.engine.scanner_engine import scan_market

router = APIRouter()


@router.get("/signal")
def get_signal(symbol: str = Query("BTCUSDT")):
    """
    Backward-compatible route.

    It returns the governed NDSP decision contract, not a raw trading signal.
    """
    return build_signal(symbol)


@router.get("/scan")
def run_scan():
    return scan_market()
