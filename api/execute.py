from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import get_db
from database.models import Execution


router = APIRouter(
    prefix="/api",
    tags=["Execution"]
)


# =========================
# Request Schema
# =========================

class ExecuteRequest(BaseModel):
    task: str



# =========================
# Execute API
# =========================

@router.post("/execute")
def execute_task(
    request: ExecuteRequest,
    db: Session = Depends(get_db)
):

    # =========================
    # TrustOS Runtime Simulation
    # (Replace with real engine later)
    # =========================

    agent = "RiskAgent"

    trust_score = 98.5

    risk_score = 1.5

    decision = "ALLOW"

    result = (
        "Completed successfully"
    )


    # =========================
    # Save Execution Audit Log
    # =========================

    execution = Execution(

        task=request.task,

        agent=agent,

        trust_score=trust_score,

        risk_score=risk_score,

        decision=decision,

        result=result
    )


    db.add(execution)

    db.commit()

    db.refresh(execution)



    # =========================
    # API Response
    # =========================

    return {

        "execution_id": execution.id,

        "status": "success",

        "task": execution.task,

        "agent": execution.agent,

        "trust_score": execution.trust_score,

        "risk_score": execution.risk_score,

        "decision": execution.decision,

        "result": execution.result,

        "created_at": execution.created_at

    }