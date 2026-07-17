from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from database.session import get_db


from schemas.execution import (
    ExecuteRequest,
    ExecutionResponse
)


from services.execution_service import ExecutionService



# ==================================================
# TrustOSAI Execution API Router
# ==================================================

router = APIRouter(

    prefix="/api/execution",

    tags=["Execution"]

)



# ==================================================
# Runtime Service Instance
# ==================================================

execution_service = ExecutionService()



# ==================================================
# Execute Task Endpoint
# ==================================================

@router.post(

    "/",

    response_model=ExecutionResponse

)

def execute_task(

    request: ExecuteRequest,

    db: Session = Depends(get_db)

):

    """
    TrustOSAI Execution Control Plane


    Pipeline:

        API Request

             |

             v

        Execution Service

             |

             +--> Trust Engine

             +--> Risk Engine

             +--> Conflict Engine

             +--> Policy Engine

             +--> Decision Engine

             +--> Telemetry Engine

             +--> Cost Engine

             +--> Audit Engine

             |

             v

        PostgreSQL Execution Ledger

    """


    execution = execution_service.execute(

        task=request.task,

        db=db

    )


    return {


        "execution_id":
            execution.id,


        "task":
            execution.task,


        "agent":
            execution.agent,



        "governance": {


            "trust_score":
                execution.trust_score,


            "risk_score":
                execution.risk_score,


            "conflict_score":
                execution.conflict_score,


            "decision":
                execution.decision

        },



        "runtime": {


            "latency_ms":
                execution.latency_ms,


            "quality_score":
                execution.quality_score

        },



        "usage": {


            "prompt_tokens":
                execution.prompt_tokens,


            "completion_tokens":
                execution.completion_tokens

        },



        "result":
            execution.result,



        "created_at":
            execution.created_at

    }