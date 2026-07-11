from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.session import get_db
from database.models import Execution


router = APIRouter(
    prefix="/execution",
    tags=["Execution"]
)


class ExecuteRequest(BaseModel):
    task: str



@router.post("/")
def execute_task(
    request: ExecuteRequest,
    db: Session = Depends(get_db)
):

    agent = "RiskAgent"

    trust_score = 98.5

    risk_score = 1.5

    conflict_score = 0.0

    decision = "ALLOW"

    result = "Completed successfully"



    execution = Execution(

        task=request.task,

        agent=agent,

        trust_score=trust_score,

        risk_score=risk_score,

        conflict_score=conflict_score,

        decision=decision,

        result=result

    )


    db.add(execution)

    db.commit()

    db.refresh(execution)


    return {

        "execution_id": execution.id,

        "task": execution.task,

        "agent": execution.agent,

        "trust_score": execution.trust_score,

        "risk_score": execution.risk_score,

        "conflict_score": execution.conflict_score,

        "decision": execution.decision,

        "result": execution.result,

        "created_at": execution.created_at

    }