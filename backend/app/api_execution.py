from fastapi import APIRouter
from app.execution.execution_engine import execute

router = APIRouter()

@router.get("/execute")
def run(symbol: str):

    account = {
        "balance": 1000,
        "daily_loss": 0.01
    }

    return execute(symbol, account)
