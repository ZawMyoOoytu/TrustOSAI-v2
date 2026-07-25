from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database.connection import get_db

from database.models import Execution





# =====================================================
# ROUTER
# =====================================================


router = APIRouter(

    prefix="/executions",

    tags=[
        "Executions"
    ]

)







# =====================================================
# SERIALIZER
# =====================================================


def execution_response(execution):

    return {


        "execution_id":

            execution.id,



        "task":

            execution.task,



        "agent":

            execution.agent,



        "agent_id":

            execution.agent_id,



        # -------------------------
        # Governance
        # -------------------------


        "trust_score":

            execution.trust_score,



        "risk_score":

            execution.risk_score,



        "conflict_score":

            execution.conflict_score,



        "decision":

            execution.decision,



        "governance_status":

            execution.governance_status,



        "governance_level":

            execution.governance_level,



        "governance_reason":

            execution.governance_reason,



        "policy_version":

            execution.policy_version,



        # -------------------------
        # Model Routing
        # -------------------------


        "model":

            execution.model,



        "provider":

            execution.provider,



        "route":

            execution.route,



        # -------------------------
        # Result
        # -------------------------


        "result":

            execution.result,



        "execution_result":

            execution.execution_result,



        "reasoning":

            execution.reasoning,



        # -------------------------
        # Telemetry
        # -------------------------


        "runtime_ms":

            execution.runtime_ms,



        "latency_ms":

            execution.latency_ms,



        "quality_score":

            execution.quality_score,



        "prompt_tokens":

            execution.prompt_tokens,



        "completion_tokens":

            execution.completion_tokens,



        "total_tokens":

            execution.total_tokens,



        "tokens_used":

            execution.tokens_used,



        # -------------------------
        # Cost
        # -------------------------


        "cost_usd":

            execution.cost_usd,



        "currency":

            execution.currency,



        # -------------------------
        # Replay
        # -------------------------


        "execution_type":

            execution.execution_type,



        "parent_execution_id":

            execution.parent_execution_id,



        # -------------------------
        # Trace
        # -------------------------


        "execution_trace":

            execution.execution_trace,



        "telemetry":

            execution.telemetry,



        "governance_metadata":

            execution.governance_metadata,



        # -------------------------
        # Time
        # -------------------------


        "created_at":

            execution.created_at,



        "updated_at":

            execution.updated_at

    }







# =====================================================
# GET ALL EXECUTIONS
# =====================================================


@router.get("/")
def get_executions(

    db: Session = Depends(get_db)

):


    executions = (

        db.query(
            Execution
        )

        .order_by(
            Execution.id.desc()
        )

        .all()

    )



    return [

        execution_response(
            execution
        )

        for execution in executions

    ]







# =====================================================
# GET SINGLE EXECUTION
# =====================================================


@router.get("/{execution_id}")
def get_execution(

    execution_id:int,

    db:Session = Depends(get_db)

):


    execution = (

        db.query(
            Execution
        )

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



    return execution_response(

        execution

    )








# =====================================================
# DELETE EXECUTION
# =====================================================


@router.delete("/{execution_id}")
def delete_execution(

    execution_id:int,

    db:Session = Depends(get_db)

):


    execution = (

        db.query(
            Execution
        )

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



    db.delete(

        execution

    )


    db.commit()



    return {


        "success":

            True,



        "deleted_execution":

            execution_id,



        "message":

            "Execution deleted successfully"

    }







# =====================================================
# DELETE ALL EXECUTIONS
# =====================================================


@router.delete("/")
def delete_all_executions(

    db:Session = Depends(get_db)

):


    count = (

        db.query(
            Execution
        )

        .delete(
            synchronize_session=False
        )

    )


    db.commit()



    return {


        "success":

            True,


        "deleted":

            count,


        "message":

            "All executions deleted"

    }