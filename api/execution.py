from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.session import get_db
from schemas.execution import ExecuteRequest, ExecutionResponse
from services.execution_service import ExecutionService


router = APIRouter(
    prefix="/api/execution",
    tags=["Execution"]
)


service = ExecutionService()



@router.post(
    "/",
    response_model=ExecutionResponse
)
def execute_task(
    request: ExecuteRequest,
    db: Session = Depends(get_db)
):


    execution = service.execute(
        request.task,
        db
    )


    return {

        "execution_id": execution.id,

        "task": execution.task,

        "agent": execution.agent,

        "trust_score": execution.trust_score,

        "risk_score": execution.risk_score,

        "conflict_score": execution.conflict_score or 0,

        "decision": execution.decision,

        "result": execution.result,

        "quality_score": execution.quality_score or 0,

        "latency_ms": execution.latency_ms or 0,

        "created_at": execution.created_at

    }