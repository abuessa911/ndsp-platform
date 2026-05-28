from fastapi import APIRouter, Header, HTTPException
import os, time
router = APIRouter()

ADMIN_KEY = os.getenv("ADMIN_KEY", "")

@router.get("/api/admin/metrics")
async def metrics(x_admin_key: str = Header(None)):
    if not ADMIN_KEY:
        raise HTTPException(status_code=503, detail="admin key not configured on server")
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="unauthorized")
    # example payload — عدّل حسب حاجتك
    return {
        "status":"healthy",
        "service":"empire-core-api",
        "time": int(time.time()),
        "signals_count": 5,
        "notes":"This is a lightweight admin endpoint — expand as needed"
    }
