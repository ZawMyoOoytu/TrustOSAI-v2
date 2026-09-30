import json

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session


from core.runtime import TrustOSRuntime


from database.models import (
    Execution,
    Agent
)


from engines.cost_engine import CostEngine





# ==========================================================
# JSON SAFE CONVERTER
# ==========================================================


def json_safe(obj: Any):

    if isinstance(obj, datetime):

        return obj.isoformat()



    if isinstance(obj, dict):

        return {

            key: json_safe(value)

            for key, value in obj.items()

        }



    if isinstance(obj, list):

        return [

            json_safe(item)

            for item in obj

        ]



    return obj







# ==========================================================
# EXECUTION SERVICE
# ==========================================================


class ExecutionService:



    def __init__(self):

        self.runtime = TrustOSRuntime()

        self.cost_engine = CostEngine()





    # ======================================================
    # MAIN EXECUTION PIPELINE
    # ======================================================


    def execute(

        self,

        task: str,

        db: Session,

        agent=None,

        agent_name=None,

        model=None,

        provider=None,

        agent_id=None,

        execution_type="NORMAL",

        parent_execution_id=None

    ):


        runtime_failed = False



        # ==================================================
        # 1. AGENT RESOLUTION
        # ==================================================


        if agent and not agent_name:

            agent_name = agent



        registered_agent = None



        if agent_id:


            registered_agent = (

                db.query(Agent)

                .filter(
                    Agent.id == agent_id
                )

                .first()

            )



            if not registered_agent:

                raise Exception(
                    "Agent not found"
                )



            if registered_agent.status != "ACTIVE":

                raise Exception(
                    "Agent disabled"
                )



            agent_name = registered_agent.name

            model = registered_agent.model

            provider = registered_agent.provider





        elif agent_name:


            registered_agent = (

                db.query(Agent)

                .filter(
                    Agent.name == agent_name
                )

                .first()

            )








        # ==================================================
        # 2. DEFAULT CONFIG
        # ==================================================


        agent_name = (

            agent_name

            or

            "GovernanceAgent"

        )


        model = (

            model

            or

            "local"

        )


        provider = (

            provider

            or

            "local"

        )








        # ==================================================
        # 3. CREATE EXECUTION RECORD
        # ==================================================


        execution = Execution(


            task=task,


            agent=agent_name,


            agent_id=(

                registered_agent.id

                if registered_agent

                else agent_id

            ),


            model=model,


            provider=provider,



            execution_type=execution_type,


            parent_execution_id=parent_execution_id,



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




        db.add(execution)

        db.commit()

        db.refresh(execution)



        execution_id = execution.id







        # ==================================================
        # 4. TRUSTOSAI RUNTIME
        # ==================================================


        try:


            runtime_result = self.runtime.execute(


                task,


                db,


                execution_id=execution_id,


                agent=agent_name,


                model=model,


                provider=provider


            )



        except Exception as e:


            runtime_failed = True



            runtime_result = {


                "decision": "BLOCK",


                "trust_score": 0,


                "risk_score":100,


                "conflict_score":0,


                "reasoning":str(e),


                "result":{

                    "error":str(e)

                }

            }





        runtime_result = json_safe(
            runtime_result
        )







        # ==================================================
        # 5. GOVERNANCE EXTRACTION
        # ==================================================


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



        reasoning = runtime_result.get(

            "reasoning",

            None

        )







        governance = runtime_result.get(

            "governance",

            {}

        )



        if not isinstance(governance, dict):

            governance={}








        # ==================================================
        # 6. RESULT NORMALIZATION
        # ==================================================


        result_json = self.normalize_json(

            runtime_result.get(

                "result",

                {}

            )

        )



        final_model = (

            result_json.get(
                "model"
            )

            or

            model

        )



        final_provider = (

            result_json.get(
                "provider"
            )

            or

            provider

        )









        # ==================================================
        # 7. TOKEN TELEMETRY
        # ==================================================


        token_data = result_json.get(

            "token_telemetry",

            {}

        )



        if not isinstance(token_data,dict):

            token_data={}




        prompt_tokens = self.safe_int(

            token_data.get(
                "prompt_tokens",
                0
            )

        )



        completion_tokens = self.safe_int(

            token_data.get(
                "completion_tokens",
                0
            )

        )



        total_tokens = self.safe_int(

            token_data.get(

                "total_tokens",

                prompt_tokens + completion_tokens

            )

        )









        # ==================================================
        # 8. METRICS
        # ==================================================


        runtime_ms = self.safe_float(

            runtime_result.get(

                "runtime_ms",

                result_json.get(

                    "runtime_ms",

                    0

                )

            )

        )



        latency_ms = self.safe_float(

            runtime_result.get(

                "latency_ms",

                runtime_ms

            )

        )






        quality_score = self.safe_float(

            result_json.get(

                "quality_score",

                result_json.get(

                    "quality_score_qt",

                    0

                )

            )

        )








        # ==================================================
        # 9. COST
        # ==================================================


        cost = self.cost_engine.calculate(

            model=final_model,

            prompt_tokens=prompt_tokens,

            completion_tokens=completion_tokens

        )



        cost_usd = self.safe_float(

            cost.get(

                "cost_usd",

                0

            )

        )


        currency = cost.get(

            "currency",

            "USD"

        )








        # ==================================================
        # 10. TRACE
        # ==================================================


        execution_trace = {


            "execution_id":execution_id,


            "agent":agent_name,


            "model":final_model,


            "provider":final_provider,


            "decision":decision,


            "trust_score":trust_score,


            "risk_score":risk_score,


            "conflict_score":conflict_score,


            "tokens":{


                "prompt":prompt_tokens,

                "completion":completion_tokens,

                "total":total_tokens

            },


            "cost":cost,


            "runtime":runtime_result,


            "timestamp":datetime.utcnow().isoformat()

        }









        # ==================================================
        # 11. UPDATE DATABASE
        # ==================================================


        execution.model = final_model


        execution.provider = final_provider



        execution.decision = decision



        execution.status = (

            "FAILED"

            if runtime_failed

            else

            "COMPLETED"

        )



        execution.trust_score = trust_score


        execution.risk_score = risk_score


        execution.conflict_score = conflict_score




        execution.reasoning = reasoning



        execution.governance_result = decision


        execution.governance_status = decision



        execution.governance_level = (

            governance.get(

                "governance_level",

                "SAFE"

            )

        )



        execution.policy_version = (

            governance.get(

                "policy_version",

                "v1.0"

            )

        )




        execution.governance_metadata = governance





        execution.result = json.dumps(

            result_json

        )



        execution.execution_result = json.dumps(

            runtime_result

        )



        execution.execution_trace = json_safe(

            execution_trace

        )



        execution.telemetry = token_data



        execution.runtime_ms = runtime_ms


        execution.latency_ms = latency_ms


        execution.quality_score = quality_score




        execution.prompt_tokens = prompt_tokens


        execution.completion_tokens = completion_tokens


        execution.total_tokens = total_tokens



        execution.cost_usd = cost_usd


        execution.currency = currency



        execution.updated_at=datetime.utcnow()







        # ==================================================
        # 12. AGENT ANALYTICS
        # ==================================================


        if registered_agent:


            old_total = registered_agent.total_executions or 0


            old_average = registered_agent.average_trust or 0



            new_total = old_total + 1



            registered_agent.total_executions = new_total



            registered_agent.average_trust = round(

                (

                    (old_average * old_total)

                    +

                    trust_score

                )

                /

                new_total,

                2

            )








        # ==================================================
        # 13. COMMIT
        # ==================================================


        db.commit()


        db.refresh(execution)



        return execution







    # ======================================================
    # JSON NORMALIZER
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






    # ======================================================
    # SAFE FLOAT
    # ======================================================


    def safe_float(self,value):

        try:

            return float(value or 0)

        except:

            return 0.0







    # ======================================================
    # SAFE INT
    # ======================================================


    def safe_int(self,value):

        try:

            return int(value or 0)

        except:

            return 0