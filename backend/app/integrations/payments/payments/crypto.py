from fastapi import APIRouter
from app.payments.core import activate_user

router=APIRouter()

@router.post("/crypto")
def crypto(email:str,plan:str="elite",tx:str=""):
    return activate_user(email,plan)
