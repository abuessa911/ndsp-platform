from fastapi import APIRouter
from app.execution.execution_optimizer import ExecutionOptimizer

router = APIRouter()
optimizer = ExecutionOptimizer()

@router.get("/execution/optimize")
def optimize():
    return optimizer.suggest()
