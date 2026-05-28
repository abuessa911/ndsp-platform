from fastapi import APIRouter
from app.services.keys import create_key

router=APIRouter()

@router.post("/create_key")
def create(user_id:int):
    key=create_key(user_id)
    return {"api_key":key}
