from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from datetime import datetime

import json


from database.session import get_db

from database.models import Execution

from core.orchestrator import RuntimeOrchestrator




# =====================================================
# ROUTER
# =====================================================

router = APIRouter(

    prefix="/replay",

    tags=[
        "Execution Replay Engine"
    ]

)




# =====================================================
# RUNTIME INSTANCE
# =====================================================

replay_runtime = RuntimeOrchestrator()





# =====================================================
# JSON SAFE CONVERTER
# =====================================================

def json_safe(obj):


    if isinstance(
        obj,
        datetime
    ):

        return obj.isoformat()



    if isinstance(
        obj,
        dict
    ):

        return {

            k: json_safe(v)

            for k,v in obj.items()

        }



    if isinstance(
        obj,
        list
    ):

        return [

            json_safe(x)

            for x in obj

        ]



    return obj







# =====================================================
# REPLAY EXECUTION
# =====================================================


@router.post(
    "/{execution_id}"
)
def replay_execution(

    execution_id:int,

    db:Session = Depends(get_db)

):


    try:



        # =================================================
        # LOAD ORIGINAL EXECUTION
        # =================================================


        original = (

            db.query(Execution)

            .filter(
                Execution.id == execution_id
            )

            .first()

        )



        if not original:


            raise HTTPException(

                status_code=404,

                detail="Original execution not found"

            )








        # =================================================
        # CREATE REPLAY RECORD
        # =================================================


        replay_record = Execution(


            task =
                original.task,


            agent =
                original.agent,


            agent_id =
                original.agent_id,


            model =
                original.model,


            provider =
                original.provider,



            execution_type =
                "REPLAY",



            parent_execution_id =
                original.id,



            decision =
                "RUNNING",



            status =
                "RUNNING",



            trust_score = 0,


            risk_score = 0,


            conflict_score = 0,



            runtime_ms = 0,


            latency_ms = 0,


            quality_score = 0,



            prompt_tokens = 0,


            completion_tokens = 0,


            total_tokens = 0,



            cost_usd = 0,


            currency = "USD"


        )





        db.add(
            replay_record
        )


        db.commit()


        db.refresh(
            replay_record
        )



        replay_id = replay_record.id







        # =================================================
        # RUN REPLAY PIPELINE
        # =================================================


        replay_result = replay_runtime.execute(


            task =
                original.task,


            db =
                db,


            execution_id =
                replay_id,


            agent =
                original.agent,


            model =
                original.model,


            provider =
                original.provider,


            user_role =
                "replay-engine",


            execution_mode =
                "REPLAY"


        )





        replay_result = json_safe(

            replay_result

        )









        # =================================================
        # UPDATE GOVERNANCE DATA
        # =================================================


        replay_record.decision = (

            replay_result.get(

                "decision",

                "BLOCK"

            )

        )



        replay_record.trust_score = (

            replay_result.get(

                "trust_score",

                0

            )

        )



        replay_record.risk_score = (

            replay_result.get(

                "risk_score",

                0

            )

        )



        replay_record.conflict_score = (

            replay_result.get(

                "conflict_score",

                0

            )

        )



        replay_record.status = "COMPLETED"










        # =================================================
        # TELEMETRY
        # =================================================


        telemetry = replay_result.get(

            "telemetry",

            {}

        )



        replay_record.telemetry = telemetry



        replay_record.runtime_ms = (

            replay_result.get(

                "runtime_ms",

                0

            )

        )



        replay_record.latency_ms = (

            replay_result.get(

                "latency_ms",

                0

            )

        )



        replay_record.quality_score = (

            replay_result.get(

                "quality_score",

                0

            )

        )









        # =================================================
        # TOKEN TELEMETRY
        # =================================================


        tokens = replay_result.get(

            "token_telemetry",

            {}

        )



        if isinstance(tokens,dict):


            replay_record.prompt_tokens = (

                tokens.get(
                    "prompt_tokens",
                    0
                )

            )


            replay_record.completion_tokens = (

                tokens.get(
                    "completion_tokens",
                    0
                )

            )


            replay_record.total_tokens = (

                tokens.get(
                    "total_tokens",
                    0
                )

            )









        # =================================================
        # SAVE RESULT
        # =================================================


        replay_record.execution_result = json.dumps(

            replay_result

        )




        replay_record.result = json.dumps(

            {

                "execution_mode":
                    "REPLAY",


                "parent_execution_id":
                    original.id,


                "result":
                    replay_result

            }

        )






        replay_record.execution_trace = {


            "engine":

                "ExecutionReplayEngine",



            "original_execution":

                original.id,



            "replay_execution":

                replay_id,



            "timestamp":

                datetime.utcnow().isoformat()

        }





        replay_record.updated_at = datetime.utcnow()



        db.commit()


        db.refresh(
            replay_record
        )









        # =================================================
        # FRONTEND COMPATIBLE RESPONSE
        # =================================================


        return {


            "replay":

                True,



            "original_execution_id":

                original.id,



            "replay_execution_id":

                replay_record.id,




            "replay_result":

            {



                "execution_id":

                    replay_record.id,



                "task":

                    original.task,



                "agent":

                    original.agent,



                "agent_id":

                    original.agent_id,



                "model":

                    original.model,



                "provider":

                    original.provider,



                "execution_type":

                    "REPLAY",



                "parent_execution_id":

                    original.id,



                "decision":

                    replay_record.decision,



                "trust_score":

                    replay_record.trust_score,



                "risk_score":

                    replay_record.risk_score,



                "conflict_score":

                    replay_record.conflict_score,



                "runtime_ms":

                    replay_record.runtime_ms,



                "latency_ms":

                    replay_record.latency_ms,



                "quality_score":

                    replay_record.quality_score,



                "token_telemetry":

                    tokens,



                "result":

                    replay_result


            }


        }







    except HTTPException:

        raise





    except Exception as e:


        db.rollback()


        raise HTTPException(


            status_code=500,


            detail={


                "message":

                    "Replay execution failed",


                "error":

                    str(e)

            }

        )









# =====================================================
# REPLAY COMPARISON
# =====================================================


@router.get(
    "/compare/{original_id}/{replay_id}"
)
def compare_replay(


    original_id:int,


    replay_id:int,


    db:Session = Depends(get_db)


):



    original = (

        db.query(Execution)

        .filter(
            Execution.id == original_id
        )

        .first()

    )



    replay = (

        db.query(Execution)

        .filter(
            Execution.id == replay_id
        )

        .first()

    )





    if not original or not replay:


        raise HTTPException(

            status_code=404,

            detail="Execution not found"

        )







    return {



        "original":{


            "id":

                original.id,


            "decision":

                original.decision,


            "trust_score":

                original.trust_score or 0,


            "risk_score":

                original.risk_score or 0,


            "model":

                original.model

        },





        "replay":{


            "id":

                replay.id,


            "decision":

                replay.decision,


            "trust_score":

                replay.trust_score or 0,


            "risk_score":

                replay.risk_score or 0,


            "model":

                replay.model

        },





        "comparison":{


            "trust_delta":

                (replay.trust_score or 0)

                -

                (original.trust_score or 0),




            "risk_delta":

                (replay.risk_score or 0)

                -

                (original.risk_score or 0),




            "decision_changed":

                replay.decision

                !=

                original.decision,




            "model_changed":

                replay.model

                !=

                original.model


        }


    }