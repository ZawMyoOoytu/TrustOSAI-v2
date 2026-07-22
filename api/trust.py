from fastapi import APIRouter, Depends

from database.session import get_db
from database.models import Execution

from core.trust_explanation import (
    TrustExplanationEngine
)


router = APIRouter(
    prefix="/trust",
    tags=["Trust"]
)



engine = TrustExplanationEngine()



@router.get(
    "/explanation/{execution_id}"
)
def explanation(
    execution_id:int,
    db=Depends(get_db)
):


    execution = (
        db.query(Execution)
        .filter(
            Execution.id==execution_id
        )
        .first()
    )


    if not execution:

        return {
            "error":
            "Execution not found"
        }


    return engine.explain(
        execution
    )