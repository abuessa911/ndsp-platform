from fastapi import APIRouter
from app.execution.execution_learning import ExecutionLearning

router = APIRouter()
learner = ExecutionLearning()

@router.get("/execution/learning")
def get_learning():
    return learner.analyze()
