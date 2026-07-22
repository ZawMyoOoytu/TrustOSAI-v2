import time

from typing import Dict, Any, Optional

from sqlalchemy.orm import Session


from engines.memory_engine import MemoryEngine
from engines.governance_engine import GovernanceEngine
from engines.router_engine import RouterEngine
from engines.execution_engine import ExecutionEngine
from engines.telemetry_engine import TelemetryEngine
from engines.audit_engine import AuditEngine
from engines.cost_engine import CostEngine





class RuntimeOrchestrator:


    """
    =====================================================
    TrustOSAI Adaptive Execution Orchestrator v5.0
    =====================================================

    Enterprise AI Governance Runtime


    Pipeline:

    Request
        |
        v
    Memory Context
        |
        v
    Governance Engine
        |
        v
    Trust / Risk / Policy
        |
        v
    Agent Router
        |
        v
    Execution Engine
        |
        v
    Quality Evaluation
        |
        v
    Cost Attribution
        |
        v
    Telemetry
        |
        v
    Audit + Memory Feedback



    Features:

    - Agent Identity Propagation
    - Model Routing
    - Provider Routing
    - Trust Evaluation
    - Risk Detection
    - Policy Enforcement
    - Execution Replay
    - Cost Attribution
    - Telemetry
    - Memory Feedback

    """



    def __init__(self):


        self.memory_engine = MemoryEngine()


        self.governance_engine = GovernanceEngine()


        self.router_engine = RouterEngine()


        self.execution_engine = ExecutionEngine()


        self.telemetry_engine = TelemetryEngine()


        self.audit_engine = AuditEngine()


        self.cost_engine = CostEngine()






    # =====================================================
    # MAIN EXECUTION PIPELINE
    # =====================================================


    def execute(

        self,

        task: str,

        db: Session,

        execution_id=None,

        user_role="user-default-01",

        execution_mode="NORMAL",

        existing_execution=False,

        agent=None,

        model=None,

        provider=None

    ) -> Dict[str,Any]:


        start_time = time.perf_counter()



        try:



            # =================================================
            # MEMORY CONTEXT
            # =================================================


            context = self.memory_engine.retrieve_context(

                task,

                db

            )



            request = {


                "task": task,


                "context": context,


                "user_role": user_role,


                "agent": agent,


                "model": model,


                "provider": provider


            }



            # =================================================
            # GOVERNANCE ENGINE
            # =================================================


            decision, governance = (

                self.governance_engine.evaluate_request(

                    request,

                    db

                )

            )



            trust_score = float(

                governance.get(

                    "trust_score",

                    0

                )

            )


            risk_score = float(

                governance.get(

                    "risk_score",

                    0

                )

            )


            conflict_score = float(

                governance.get(

                    "conflict_score",

                    0

                )

            )
                        # =================================================
            # GOVERNANCE BLOCK
            # =================================================


            if decision == "BLOCK":


                latency = (

                    time.perf_counter()

                    -

                    start_time

                ) * 1000



                blocked_result = {


                    "execution_id":

                        execution_id,


                    "execution_mode":

                        execution_mode,


                    "task":

                        task,


                    "agent":

                        agent or "GovernanceAgent",


                    "route":

                        "GovernanceAgent",



                    "decision":

                        "BLOCK",



                    "trust_score":

                        trust_score,



                    "risk_score":

                        risk_score,



                    "conflict_score":

                        conflict_score,



                    "result":{


                        "status":

                            "BLOCKED",


                        "message":

                            "Execution blocked by governance policy"


                    },



                    "cost":{


                        "cost_usd":0,


                        "currency":"USD"


                    },



                    "governance":

                        governance,



                    "telemetry":{


                        "latency_ms":

                            round(latency,3),



                        "quality_score":

                            0


                    },



                    "runtime_ms":

                        round(latency,3)


                }




                self.audit_engine.record(

                    task,

                    trust_score,

                    risk_score,

                    governance,

                    blocked_result

                )



                return blocked_result







            # =================================================
            # AGENT ROUTING
            # =================================================


            route = self.router_engine.select_optimal_agent(



                {


                    "aggregated_trust":

                        trust_score,


                    "decision":

                        decision,


                    "risk_score":

                        risk_score



                },



                {


                    "task":

                        task,


                    "requested_agent":

                        agent,


                    "requested_model":

                        model,


                    "requested_provider":

                        provider



                }


            )




            # fallback

            if not route:


                route = agent or "GovernanceAgent"









            # =================================================
            # EXECUTION ENGINE
            # =================================================


            execution_result = self.execution_engine.execute(



                route,


                task,



                execution_id=execution_id,



                model=model,


                provider=provider



            )





            if not isinstance(execution_result,dict):


                execution_result={


                    "response":

                        str(execution_result)


                }







            # =================================================
            # MODEL PROVIDER RESOLUTION
            # =================================================



            final_model = (


                execution_result.get(

                    "model"

                )

                or

                model

                or

                "unknown"


            )




            final_provider = (


                execution_result.get(

                    "provider"

                )

                or

                provider

                or

                "local"


            )








            # =================================================
            # TOKEN TELEMETRY
            # =================================================



            token_data = execution_result.get(

                "token_telemetry",

                {}

            )



            if not isinstance(token_data,dict):

                token_data={}




            prompt_tokens = int(

                token_data.get(

                    "prompt_tokens",

                    0

                )

            )




            completion_tokens = int(

                token_data.get(

                    "completion_tokens",

                    0

                )

            )




            total_tokens = (

                prompt_tokens

                +

                completion_tokens

            )







            # =================================================
            # QUALITY SCORE
            # =================================================



            quality_score = float(

                execution_result.get(

                    "quality_score",

                    0

                )

            )



            if quality_score == 0:


                nested_result = execution_result.get(

                    "result",

                    {}

                )



                if isinstance(

                    nested_result,

                    dict

                ):


                    quality_score=float(

                        nested_result.get(

                            "quality_score",

                            0

                        )

                    )







            quality_score=round(

                quality_score,

                4

            )








            # =================================================
            # COST ENGINE
            # =================================================



            cost = self.cost_engine.calculate(



                model=final_model,



                prompt_tokens=prompt_tokens,



                completion_tokens=completion_tokens



            )
                        # =================================================
            # TELEMETRY COLLECTION
            # =================================================


            telemetry = self.telemetry_engine.collect(


                task,


                {


                    "agent": route,


                    "model": final_model,


                    "provider": final_provider,


                    "trust_score": trust_score,


                    "risk_score": risk_score,


                    "decision": decision,


                    "quality_score": quality_score



                }


            )





            latency = (

                time.perf_counter()

                -

                start_time

            ) * 1000








            # =================================================
            # MEMORY FEEDBACK UPDATE
            # =================================================


            self.memory_engine.update_memory(


                db,


                task,


                execution_result,


                quality_score



            )








            # =================================================
            # AUDIT LOGGING
            # =================================================


            self.audit_engine.record(



                task,


                trust_score,


                risk_score,


                governance,


                execution_result



            )








            # =================================================
            # FINAL RUNTIME RESPONSE
            # =================================================


            return {



                "execution_id":

                    execution_id,



                "execution_mode":

                    execution_mode,



                "task":

                    task,



                "agent":

                    route,



                "route":

                    route,



                "decision":

                    decision,



                "trust_score":

                    trust_score,



                "risk_score":

                    risk_score,



                "conflict_score":

                    conflict_score,



                "model":

                    final_model,



                "provider":

                    final_provider,





                "token_telemetry":{



                    "prompt_tokens":

                        prompt_tokens,



                    "completion_tokens":

                        completion_tokens,



                    "total_tokens":

                        total_tokens



                },




                "quality_score":

                    quality_score,




                "result":

                    execution_result,




                "cost":

                    cost,




                "governance":

                    governance,




                "telemetry":{



                    "latency_ms":

                        round(latency,3),



                    "quality_score":

                        quality_score



                },




                "runtime_ms":

                    round(latency,3)



            }









        # =====================================================
        # GLOBAL EXCEPTION HANDLER
        # =====================================================


        except Exception as e:



            latency = (

                time.perf_counter()

                -

                start_time

            ) * 1000



            return {



                "execution_id":

                    execution_id,



                "execution_mode":

                    execution_mode,



                "task":

                    task,



                "agent":

                    agent or "RuntimeOrchestrator",



                "decision":

                    "BLOCK",



                "trust_score":

                    0.0,



                "risk_score":

                    1.0,



                "conflict_score":

                    0.0,



                "result":{


                    "error":

                        str(e)



                },



                "cost":{


                    "cost_usd":0,


                    "currency":"USD"



                },



                "telemetry":{


                    "latency_ms":

                        round(latency,3),



                    "quality_score":

                        0



                },



                "runtime_ms":

                    round(latency,3)



            }









# =====================================================
# GLOBAL INSTANCE
# =====================================================


orchestrator = RuntimeOrchestrator()



# Backward Compatibility
Orchestrator = RuntimeOrchestrator