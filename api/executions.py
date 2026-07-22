from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Execution


# =====================================================
# Router
# =====================================================

router = APIRouter(
    prefix="/executions",
    tags=["Executions"]
)


# =====================================================
# GET ALL EXECUTIONS
# =====================================================

@router.get("/")
def get_executions(
    db: Session = Depends(get_db)
):

    executions = (
        db.query(Execution)
        .order_by(Execution.id.desc())
        .all()
    )

    return [
        {
            "execution_id": execution.id,
            "task": execution.task,
            "agent": execution.agent,
            "trust_score": execution.trust_score,
            "risk_score": execution.risk_score,
            "decision": execution.decision,
            "result": execution.result,
            "created_at": execution.created_at,
        }
        for execution in executions
    ]


# =====================================================
# GET SINGLE EXECUTION
# =====================================================

@router.get("/{execution_id}")
def get_execution(
    execution_id: int,
    db: Session = Depends(get_db)
):

    execution = (
        db.query(Execution)
        .filter(Execution.id == execution_id)
        .first()
    )

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )

    return {
        "execution_id": execution.id,
        "task": execution.task,
        "agent": execution.agent,
        "trust_score": execution.trust_score,
        "risk_score": execution.risk_score,
        "decision": execution.decision,
        "result": execution.result,
        "created_at": execution.created_at,
    }


# =====================================================
# DELETE EXECUTION
# =====================================================

@router.delete("/{execution_id}")
def delete_execution(
    execution_id: int,
    db: Session = Depends(get_db)
):

    execution = (
        db.query(Execution)
        .filter(Execution.id == execution_id)
        .first()
    )

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )

    db.delete(execution)
    db.commit()

    return {
        "success": True,
        "message": f"Execution #{execution_id} deleted successfully"
    }


# =====================================================
# DELETE ALL EXECUTIONS (Optional)
# =====================================================

@router.delete("/")
def delete_all_executions(
    db: Session = Depends(get_db)
):

    deleted = (
        db.query(Execution)
        .delete(synchronize_session=False)
    )

    db.commit()

    return {
        "success": True,
        "deleted": deleted,
        "message": "All executions deleted successfully"
    }