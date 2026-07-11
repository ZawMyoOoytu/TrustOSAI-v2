from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Execution



router = APIRouter(
    prefix="/executions",
    tags=["Executions"]
)



# ==========================
# GET ALL EXECUTIONS
# ==========================

@router.get("/")
def get_executions(
    db: Session = Depends(get_db)
):

    executions = (
        db.query(Execution)
        .order_by(
            Execution.id.desc()
        )
        .all()
    )


    return executions



# ==========================
# GET SINGLE EXECUTION
# ==========================

@router.get("/{execution_id}")
def get_execution(
    execution_id:int,
    db:Session = Depends(get_db)
):

    execution = (
        db.query(Execution)
        .filter(
            Execution.id == execution_id
        )
        .first()
    )


    if execution is None:

        raise HTTPException(
            status_code=404,
            detail="Execution not found"
        )


    return execution