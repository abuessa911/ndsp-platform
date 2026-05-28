from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/api/runtime/health")
def runtime_health():
    return {
        "ok": True,
        "service": "ndsp-api",
        "database": os.environ.get("PGDATABASE", "unknown"),
        "db_user": os.environ.get("PGUSER", "unknown"),
        "password_exposed": False,
    }
