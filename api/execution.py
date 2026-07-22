from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database.session import get_db

from database.models import (
    Agent,
    Execution
)

from schemas.execution import (
    ExecuteRequest,
    ExecutionResponse,
    CostResponse,
    TokenTelemetryResponse
)

from services.execution_service import ExecutionService

import json





# =====================================================
# ROUTER
# =====================================================

router = APIRouter(
    prefix="/api/execution",
    tags=["Execution"]
)





# =====================================================
# SERVICE
# =====================================================

service = ExecutionService()







# =====================================================
# POST EXECUTION
# =====================================================


@router.post(
    "/",
    response_model=ExecutionResponse
)
def execute_task(
    request: ExecuteRequest,
    db: Session = Depends(get_db)
):


    # =================================================
    # 1. FIND AGENT
    # =================================================


    selected_agent = None


    if request.agent_id:


        selected_agent = (
            db.query(Agent)
            .filter(
                Agent.id == request.agent_id
            )
            .first()
        )


        if not selected_agent:

            raise HTTPException(
                status_code=404,
                detail="Agent not found"
            )



        if selected_agent.status != "ACTIVE":

            raise HTTPException(
                status_code=403,
                detail="Agent disabled"
            )







    # =================================================
    # 2. RUNTIME CONFIG
    # =================================================


    if selected_agent:


        agent_name = selected_agent.name

        model = selected_agent.model

        provider = selected_agent.provider



    else:


        agent_name = (
            request.agent
            or
            "TrustOSAI Runtime Agent"
        )


        model = (
            request.model
            or
            "local"
        )


        provider = (
            request.provider
            or
            "local"
        )








    # =================================================
    # 3. EXECUTION
    # =================================================


    execution = service.execute(

        task=request.task,

        db=db,

        agent=agent_name,

        model=model,

        provider=provider

    )







    # =================================================
    # 4. PARSE RESULT
    # =================================================


    token_data = {

        "prompt_tokens":0,

        "completion_tokens":0,

        "total_tokens":0,

        "context_window":8000

    }



    final_model = model


    final_provider = provider



    try:


        data = json.loads(
            execution.result
        )


        final_model = data.get(
            "model",
            model
        )


        token_data = data.get(
            "token_telemetry",
            token_data
        )


        trace = data.get(
            "trace",
            {}
        )


        output = trace.get(
            "output",
            {}
        )


        final_provider = output.get(
            "provider",
            provider
        )



    except Exception:


        pass








    # =================================================
    # 5. UPDATE AGENT ANALYTICS
    # =================================================


    if selected_agent:


        total = (
            db.query(Execution)
            .filter(
                Execution.agent_id ==
                selected_agent.id
            )
            .count()
        )


        selected_agent.total_executions = total



        if total:


            avg = (

                db.query(
                    Execution
                )
                .filter(
                    Execution.agent_id ==
                    selected_agent.id
                )
                .with_entities(
                    Execution.trust_score
                )
                .all()

            )


            selected_agent.average_trust = round(

                sum(
                    x[0]
                    for x in avg
                )
                /
                total,

                2

            )


        db.commit()








    # =================================================
    # 6. RESPONSE
    # =================================================


    return ExecutionResponse(



        execution_id=execution.id,


        task=execution.task,


        agent=execution.agent,


        agent_id=execution.agent_id,




        # Governance

        trust_score=execution.trust_score or 0,


        risk_score=execution.risk_score or 0,


        conflict_score=execution.conflict_score or 0,


        decision=execution.decision,



        reasoning=execution.governance_reason,






        # Result

        result=execution.result,


        status="COMPLETED",






        # Telemetry


        quality_score=execution.quality_score or 0,


        latency_ms=execution.latency_ms or 0,


        runtime_ms=execution.runtime_ms or 0,







        # Model


        provider=final_provider,


        model=final_model,







        # Cost


        cost=CostResponse(

            input_tokens=token_data.get(
                "prompt_tokens",
                0
            ),

            output_tokens=token_data.get(
                "completion_tokens",
                0
            ),

            total_tokens=token_data.get(
                "total_tokens",
                0
            ),

            total_cost=execution.cost_usd or 0,


            currency=execution.currency or "USD"

        ),







        # Token


        token_telemetry=TokenTelemetryResponse(

            prompt_tokens=token_data.get(
                "prompt_tokens",
                0
            ),


            completion_tokens=token_data.get(
                "completion_tokens",
                0
            ),


            total_tokens=token_data.get(
                "total_tokens",
                0
            ),


            context_window=token_data.get(
                "context_window",
                8000
            )

        ),






        # Replay


        execution_type=execution.execution_type or "NORMAL",


        parent_execution_id=execution.parent_execution_id,






        metadata_json=request.metadata_json,



        created_at=execution.created_at

    )