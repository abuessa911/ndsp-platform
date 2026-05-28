from fastapi import APIRouter
from app.services.winrate_engine import get_stats

router = APIRouter()

@router.get("/stats")
def stats():
    return get_stats()
