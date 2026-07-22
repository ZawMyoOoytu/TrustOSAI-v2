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
# JSON SAFE
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
        # 1. LOAD ORIGINAL EXECUTION
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
        # 2. CREATE REPLAY EXECUTION RECORD
        # =================================================


        replay_record = Execution(



            task = original.task,



            agent = original.agent,



            agent_id = original.agent_id,



            model = original.model,



            provider = original.provider,



            execution_type="REPLAY",



            parent_execution_id=original.id,



            decision="RUNNING",



            status="RUNNING",



            trust_score=0,



            risk_score=0,



            conflict_score=0,



            runtime_ms=0,


            latency_ms=0,


            quality_score=0,



            prompt_tokens=0,


            completion_tokens=0,


            total_tokens=0,



            cost_usd=0,


            currency="USD"


        )





        db.add(replay_record)


        db.commit()


        db.refresh(replay_record)



        replay_id = replay_record.id







        # =================================================
        # 3. EXECUTE REPLAY PIPELINE
        # =================================================


        replay_result = replay_runtime.execute(


            task=original.task,


            db=db,


            execution_id=replay_id,


            agent=original.agent,


            model=original.model,


            provider=original.provider,


            user_role="replay-engine",


            execution_mode="REPLAY"


        )







        replay_result = json_safe(

            replay_result

        )







        # =================================================
        # 4. EXTRACT GOVERNANCE RESULT
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
        # 5. TELEMETRY UPDATE
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
        # 6. TOKEN DATA
        # =================================================


        token_data = replay_result.get(

            "token_telemetry",

            {}

        )



        if isinstance(

            token_data,

            dict

        ):



            replay_record.prompt_tokens = (

                token_data.get(

                    "prompt_tokens",

                    0

                )

            )



            replay_record.completion_tokens = (

                token_data.get(

                    "completion_tokens",

                    0

                )

            )



            replay_record.total_tokens = (

                token_data.get(

                    "total_tokens",

                    0

                )

            )







        # =================================================
        # 7. SAVE TRACE
        # =================================================


        replay_record.execution_result = json.dumps(

            replay_result

        )



        replay_record.result = json.dumps(

            {

                "execution_mode":"REPLAY",

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


        db.refresh(replay_record)







        # =================================================
        # RESPONSE
        # =================================================


        return {



            "replay": True,



            "original_execution_id":

                original.id,



            "replay_execution_id":

                replay_record.id,




            "execution_type":

                "REPLAY",




            "parent_execution_id":

                original.id,




            "replay_result":

            {


                **replay_result,



                "execution_id":

                    replay_record.id,



                "execution_type":

                    "REPLAY",



                "parent_execution_id":

                    original.id


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

                original.trust_score,


            "risk_score":

                original.risk_score,


            "model":

                original.model


        },



        "replay":{


            "id":

                replay.id,


            "decision":

                replay.decision,


            "trust_score":

                replay.trust_score,


            "risk_score":

                replay.risk_score,


            "model":

                replay.model


        },



        "comparison":{


            "trust_delta":

                replay.trust_score
                -
                original.trust_score,



            "risk_delta":

                replay.risk_score
                -
                original.risk_score,



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