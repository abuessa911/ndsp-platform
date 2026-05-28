from fastapi import APIRouter
from app.core.governed_pipeline import run_governed
from app.execution.execution_engine import execute

router = APIRouter()

@router.get("/execute")
def run(symbol: str):

    result = run_governed(symbol)

    execution = execute(symbol, result["decision"])

    return {
        "decision": result["decision"],
        "execution": execution
    }
