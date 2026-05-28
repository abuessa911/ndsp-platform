from fastapi import APIRouter, Request
from app.payments.core import activate_user

router=APIRouter()

@router.post("/paddle")
async def paddle(request:Request):
    data=await request.json()

    email=data.get("email","paddle@user")
    plan=data.get("plan","pro")

    return activate_user(email,plan)
