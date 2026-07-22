from fastapi import APIRouter, Depends


from database.session import get_db

from database.models import Execution


from core.decision_reasoning import (
    DecisionReasoningEngine
)



router = APIRouter(

    prefix="/reasoning",

    tags=["Decision Reasoning"]

)



engine = DecisionReasoningEngine()




@router.get(
    "/{execution_id}"
)
def get_reasoning(

    execution_id:int,

    db=Depends(get_db)

):


    execution = (

        db.query(Execution)

        .filter(
            Execution.id == execution_id
        )

        .first()

    )



    if not execution:

        return {

            "error":
            "Execution not found"

        }



    return engine.generate(
        execution
    )