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

    prefix="/execution",

    tags=[
        "Execution"
    ]

)







# =====================================================
# SERVICE INSTANCE
# =====================================================


service = ExecutionService()







# =====================================================
# JSON PARSER
# =====================================================


def parse_json(value):


    if value is None:

        return None



    if isinstance(
        value,
        dict
    ):

        return value



    try:

        return json.loads(
            value
        )


    except Exception:


        return {

            "response": value

        }









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
    # 1. AGENT RESOLUTION
    # =================================================


    selected_agent = None



    if request.agent_id:


        selected_agent = (

            db.query(
                Agent
            )

            .filter(
                Agent.id ==
                request.agent_id
            )

            .first()

        )



        if selected_agent is None:


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
    # 2. RUNTIME CONFIGURATION
    # =================================================


    if selected_agent:


        agent_name = selected_agent.name


        model = selected_agent.model


        provider = selected_agent.provider



        agent_id = selected_agent.id



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


        agent_id = None







    # =================================================
    # 3. EXECUTION PIPELINE
    # =================================================


    execution = service.execute(

        task=request.task,

        db=db,

        agent=agent_name,

        agent_id=agent_id,

        model=model,

        provider=provider

    )









    # =================================================
    # 4. RESULT EXTRACTION
    # =================================================


    token_data = {


        "prompt_tokens":0,


        "completion_tokens":0,


        "total_tokens":0,


        "context_window":8000

    }



    final_model = model


    final_provider = provider






    parsed_result = parse_json(

        execution.result

    )




    if isinstance(
        parsed_result,
        dict
    ):



        final_model = parsed_result.get(

            "model",

            model

        )



        token_data = parsed_result.get(

            "token_telemetry",

            token_data

        )



        trace = parsed_result.get(

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









    # =================================================
    # 5. UPDATE EXECUTION STATUS
    # =================================================


    execution.status = "COMPLETED"


    db.commit()


    db.refresh(
        execution
    )









    # =================================================
    # 6. UPDATE AGENT ANALYTICS
    # =================================================


    if selected_agent:



        total = (

            db.query(
                Execution
            )

            .filter(

                Execution.agent_id

                ==

                selected_agent.id

            )

            .count()

        )



        selected_agent.total_executions = total





        if total > 0:


            values = (

                db.query(

                    Execution.trust_score

                )

                .filter(

                    Execution.agent_id

                    ==

                    selected_agent.id

                )

                .all()

            )



            selected_agent.average_trust = round(

                sum(

                    item[0] or 0

                    for item in values

                )

                /

                total,

                2

            )



        db.commit()











    # =================================================
    # 7. RESPONSE
    # =================================================


    return ExecutionResponse(




        execution_id=execution.id,



        task=execution.task,



        agent=execution.agent,



        agent_id=execution.agent_id,







        # -------------------------
        # GOVERNANCE
        # -------------------------


        trust_score=execution.trust_score or 0,


        risk_score=execution.risk_score or 0,


        conflict_score=execution.conflict_score or 0,



        decision=execution.decision,



        reasoning=(

            execution.governance_reason

            or

            execution.reasoning

        ),







        # -------------------------
        # RESULT
        # -------------------------


        result=parsed_result,



        status=execution.status,







        # -------------------------
        # TELEMETRY
        # -------------------------


        quality_score=(

            execution.quality_score

            or

            0

        ),



        latency_ms=(

            execution.latency_ms

            or

            0

        ),



        runtime_ms=(

            execution.runtime_ms

            or

            0

        ),







        # -------------------------
        # MODEL
        # -------------------------


        model=final_model,


        provider=final_provider,







        # -------------------------
        # COST
        # -------------------------


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



            total_cost=(

                execution.cost_usd

                or

                0

            ),



            currency=(

                execution.currency

                or

                "USD"

            )

        ),







        # -------------------------
        # TOKEN TELEMETRY
        # -------------------------


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







        # -------------------------
        # REPLAY
        # -------------------------


        execution_type=(

            execution.execution_type

            or

            "NORMAL"

        ),



        parent_execution_id=(

            execution.parent_execution_id

        ),







        metadata_json=request.metadata_json,



        created_at=execution.created_at



    )