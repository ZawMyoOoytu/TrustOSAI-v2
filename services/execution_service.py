import json

from datetime import datetime
from typing import Any, Dict

from sqlalchemy.orm import Session

from core.runtime import TrustOSRuntime
from database.models import Execution



# ==========================================================
# JSON SAFE
# ==========================================================

def json_safe(obj: Any):

    if isinstance(obj, datetime):
        return obj.isoformat()


    if isinstance(obj, dict):

        return {
            k: json_safe(v)
            for k, v in obj.items()
        }


    if isinstance(obj, list):

        return [
            json_safe(v)
            for v in obj
        ]


    if isinstance(obj, tuple):

        return [
            json_safe(v)
            for v in obj
        ]


    return obj





# ==========================================================
# SERVICE
# ==========================================================


class ExecutionService:


    def __init__(self):

        self.runtime = TrustOSRuntime()



    # ======================================================
    # EXECUTE
    # ======================================================


    def execute(
        self,
        task: str,
        db: Session
    ):


        runtime_result = self.runtime.execute(
            task,
            db
        )


        runtime_result = json_safe(
            runtime_result
        )



        decision = runtime_result.get(
            "decision",
            "BLOCK"
        )


        trust_score = self.safe_float(
            runtime_result.get(
                "trust_score",
                0
            )
        )


        risk_score = self.safe_float(
            runtime_result.get(
                "risk_score",
                0
            )
        )


        conflict_score = self.safe_float(
            runtime_result.get(
                "conflict_score",
                0
            )
        )



        agent = (

            runtime_result.get("agent")

            or

            runtime_result.get("route")

            or

            "GovernanceAgent"

        )



        governance_reason = (

            runtime_result.get("reason")

            or

            runtime_result.get("governance_reason")

        )



        # =============================
        # RESULT
        # =============================


        result_json = self.normalize_json(

            runtime_result.get(
                "result",
                {}
            )

        )




        # =============================
        # TELEMETRY
        # =============================


        telemetry = runtime_result.get(
            "telemetry",
            {}
        )


        latency_ms = self.safe_float(

            telemetry.get(
                "latency_ms",
                runtime_result.get(
                    "runtime_ms",
                    0
                )
            )

        )


        runtime_ms = self.safe_float(

            runtime_result.get(
                "runtime_ms",
                latency_ms
            )

        )



        quality_score = self.extract_quality(

            result_json,

            telemetry,

            decision

        )





        # =============================
        # TOKEN
        # =============================


        token = result_json.get(
            "token_telemetry",
            {}
        )


        prompt_tokens = self.safe_int(

            token.get(
                "prompt_tokens",
                0
            )

        )


        completion_tokens = self.safe_int(

            token.get(
                "completion_tokens",
                0
            )

        )




        # =============================
        # COST
        # =============================


        cost = runtime_result.get(
            "cost",
            {}
        )


        if isinstance(cost,dict):

            cost_usd = self.safe_float(

                cost.get(
                    "cost_usd",
                    0
                )

            )

        else:

            cost_usd = self.safe_float(cost)




        # =============================
        # TRACE
        # =============================


        execution_trace = {

            "runtime":

                runtime_result,


            "stored_at":

                datetime.utcnow().isoformat()

        }





        # =============================
        # DATABASE
        # =============================


        execution = Execution(


            task=task,


            agent=agent,


            route=agent,


            trust_score=trust_score,


            risk_score=risk_score,


            conflict_score=conflict_score,


            decision=decision,


            policy_result=decision,


            governance_result=decision,


            governance_status=decision,


            governance_reason=governance_reason,



            result=json.dumps(
                result_json
            ),


            execution_result=json.dumps(
                result_json
            ),



            execution_trace=execution_trace,



            runtime_ms=runtime_ms,


            latency_ms=latency_ms,


            quality_score=quality_score,


            prompt_tokens=prompt_tokens,


            completion_tokens=completion_tokens,


            cost_usd=cost_usd

        )



        try:

            db.add(execution)

            db.commit()

            db.refresh(execution)


        except Exception:

            db.rollback()

            raise



        return execution





    # ======================================================
    # QUALITY
    # ======================================================


    def extract_quality(
        self,
        result,
        telemetry,
        decision
    ):


        if isinstance(result,str):

            try:

                result=json.loads(result)

            except:

                result={}




        # direct

        if "quality_score" in result:

            return self.safe_float(

                result["quality_score"]

            )



        if "quality_score_qt" in result:

            return self.safe_float(

                result["quality_score_qt"]

            )



        # nested trace

        trace=result.get(
            "trace",
            {}
        )


        if isinstance(trace,dict):

            output=trace.get(
                "output",
                {}
            )


            if isinstance(output,dict):

                if "quality_score" in output:

                    return self.safe_float(

                        output["quality_score"]

                    )




        if isinstance(telemetry,dict):

            if "quality_score" in telemetry:

                return self.safe_float(

                    telemetry["quality_score"]

                )




        if decision=="ALLOW":

            return 1.0


        if decision=="ALLOW_WITH_MONITORING":

            return 0.8


        if decision=="REVIEW":

            return 0.5


        return 0.0





    # ======================================================
    # HELPERS
    # ======================================================


    def normalize_json(self,data):

        if isinstance(data,str):

            try:

                return json.loads(data)

            except:

                return {
                    "response":data
                }


        if isinstance(data,dict):

            return data


        return {}




    def safe_float(self,value):

        try:

            return float(value)

        except:

            return 0.0



    def safe_int(self,value):

        try:

            return int(value)

        except:

            return 0