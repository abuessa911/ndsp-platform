from fastapi import APIRouter
from app.execution.mode_config import set_mode, get_mode

router = APIRouter()

@router.get("/mode")
def current():
    return {"mode": get_mode()}

@router.get("/mode/set")
def change(mode: str):
    return set_mode(mode.upper())
