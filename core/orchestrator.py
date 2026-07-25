import time

from typing import Dict, Any, Optional

from sqlalchemy.orm import Session


# =====================================================
# EXISTING TRUSTOSAI ENGINES
# =====================================================

from engines.memory_engine import MemoryEngine
from engines.governance_engine import GovernanceEngine
from engines.router_engine import RouterEngine
from engines.execution_engine import ExecutionEngine
from engines.telemetry_engine import TelemetryEngine
from engines.audit_engine import AuditEngine
from engines.cost_engine import CostEngine



# =====================================================
# MULTI MODEL ROUTING LAYER
# =====================================================

from router.model_registry import ModelRegistry

from router.router_engine import (
    RouterEngine as ModelRouterEngine
)

from router.provider_manager import ProviderManager





class RuntimeOrchestrator:


    """
    =====================================================
    TrustOSAI Adaptive Execution Orchestrator v6.0
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
    Adaptive Model Router
        |
        v
    Provider Manager
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
    Audit Logging
        |
        v
    Memory Feedback



    Features:

    - Agent Identity Propagation
    - Agent Routing
    - Multi Model Routing
    - Provider Routing
    - Trust Evaluation
    - Risk Detection
    - Policy Enforcement
    - Execution Replay
    - Token Telemetry
    - Quality Evaluation
    - Cost Attribution
    - Runtime Telemetry
    - Audit Logging
    - Memory Learning

    =====================================================
    """



    def __init__(self):


        # =================================================
        # CORE TRUSTOSAI RUNTIME
        # =================================================


        self.memory_engine = MemoryEngine()


        self.governance_engine = GovernanceEngine()


        # Agent Router

        self.router_engine = RouterEngine()


        self.execution_engine = ExecutionEngine()


        self.telemetry_engine = TelemetryEngine()


        self.audit_engine = AuditEngine()


        self.cost_engine = CostEngine()





        # =================================================
        # ADAPTIVE MULTI MODEL ROUTER
        # =================================================


        self.model_registry = ModelRegistry()


        self.model_router_engine = ModelRouterEngine()


        self.provider_manager = ProviderManager()







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

    ) -> Dict[str, Any]:



        start_time = time.perf_counter()



        try:



            # =================================================
            # 1. MEMORY CONTEXT
            # =================================================


            context = (

                self.memory_engine
                .retrieve_context(

                    task,

                    db

                )

            )




            request = {


                "task":

                    task,


                "context":

                    context,


                "user_role":

                    user_role,


                "agent":

                    agent,


                "model":

                    model,


                "provider":

                    provider


            }





            # =================================================
            # 2. GOVERNANCE ENGINE
            # =================================================


            decision, governance = (

                self.governance_engine
                .evaluate_request(

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
            # 3. GOVERNANCE BLOCK
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


                        "cost_usd":

                            0,


                        "currency":

                            "USD"


                    },



                    "governance":

                        governance,



                    "telemetry":{


                        "latency_ms":

                            round(

                                latency,

                                3

                            ),


                        "quality_score":

                            0


                    },



                    "runtime_ms":

                        round(

                            latency,

                            3

                        )


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
            # 4. AGENT ROUTING
            # =================================================


            route = (

                self.router_engine
                .select_optimal_agent(



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

            )




            if not route:


                route = (

                    agent

                    or

                    "GovernanceAgent"

                )







            # =================================================
            # 5. ADAPTIVE MODEL ROUTING
            # =================================================


            available_models = (

                self.model_registry
                .get_models()

            )




            selected_model_result, model_ranking = (

                self.model_router_engine
                .select(

                    available_models

                )

            )




            selected_model = (

                selected_model_result
                .get(

                    "model"

                )

                if isinstance(

                    selected_model_result,

                    dict

                )

                else None

            )




            routing_score = (

                selected_model_result
                .get(

                    "routing_score",

                    0

                )

                if isinstance(

                    selected_model_result,

                    dict

                )

                else 0

            )




            if not selected_model:


                selected_model = {


                    "name":

                        model or "llama-3-70b",



                    "provider":

                        provider or "local"


                }





            selected_model_name = (

                selected_model
                .get(

                    "name"

                )

            )




            selected_provider = (

                selected_model
                .get(

                    "provider"

                )

            )
                        # =================================================
            # 6. EXECUTION ENGINE
            # =================================================


            execution_result = (

                self.execution_engine
                .execute(


                    route,


                    task,



                    execution_id=execution_id,



                    model=selected_model_name,



                    provider=selected_provider



                )

            )





            if not isinstance(

                execution_result,

                dict

            ):


                execution_result = {


                    "response":

                        str(

                            execution_result

                        ),



                    "model":

                        selected_model_name,



                    "provider":

                        selected_provider


                }








            # =================================================
            # 7. MODEL PROVIDER RESOLUTION
            # =================================================


            final_model = (

                execution_result
                .get(

                    "model"

                )

                or

                selected_model_name

                or

                model

                or

                "unknown"

            )





            final_provider = (

                execution_result
                .get(

                    "provider"

                )

                or

                selected_provider

                or

                provider

                or

                "local"

            )









            # =================================================
            # 8. TOKEN TELEMETRY
            # =================================================


            token_data = (

                execution_result
                .get(

                    "token_telemetry",

                    {}

                )

            )




            if not isinstance(

                token_data,

                dict

            ):

                token_data = {}





            prompt_tokens = int(

                token_data
                .get(

                    "prompt_tokens",

                    0

                )

            )




            completion_tokens = int(

                token_data
                .get(

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
            # 9. QUALITY EVALUATION
            # =================================================


            quality_score = float(

                execution_result
                .get(

                    "quality_score",

                    0

                )

            )





            if quality_score == 0:


                nested_result = (

                    execution_result
                    .get(

                        "result",

                        {}

                    )

                )




                if isinstance(

                    nested_result,

                    dict

                ):



                    quality_score = float(

                        nested_result
                        .get(

                            "quality_score",

                            nested_result
                            .get(

                                "quality_score_qt",

                                0

                            )

                        )

                    )






            quality_score = round(

                quality_score,

                4

            )









            # =================================================
            # 10. COST ATTRIBUTION
            # =================================================


            cost = (

                self.cost_engine
                .calculate(



                    model=

                        final_model,



                    prompt_tokens=

                        prompt_tokens,



                    completion_tokens=

                        completion_tokens



                )

            )









            # =================================================
            # 11. TELEMETRY COLLECTION
            # =================================================


            telemetry = (

                self.telemetry_engine
                .collect(


                    task,



                    {


                        "agent":

                            route,



                        "model":

                            final_model,



                        "provider":

                            final_provider,



                        "trust_score":

                            trust_score,



                        "risk_score":

                            risk_score,



                        "decision":

                            decision,



                        "quality_score":

                            quality_score,



                        "routing_score":

                            routing_score,



                        "routing_strategy":

                            "TRUST_OPTIMIZED",



                        "tokens":

                            total_tokens


                    }



                )

            )








            latency = (

                time.perf_counter()

                -

                start_time

            ) * 1000









            # =================================================
            # 12. MEMORY FEEDBACK UPDATE
            # =================================================


            self.memory_engine.update_memory(



                db,



                task,



                execution_result,



                quality_score



            )









            # =================================================
            # 13. AUDIT LOGGING
            # =================================================


            self.audit_engine.record(



                task,



                trust_score,



                risk_score,



                governance,



                execution_result



            )









            # =================================================
            # 14. FINAL RUNTIME RESPONSE
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







                "routing":{


                    "strategy":

                        "TRUST_OPTIMIZED",



                    "selected":{


                        "model":

                            final_model,



                        "provider":

                            final_provider,



                        "routing_score":

                            routing_score



                    },



                    "ranking":

                        model_ranking



                },








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

                        round(

                            latency,

                            3

                        ),



                    "quality_score":

                        quality_score



                },







                "runtime_ms":

                    round(

                        latency,

                        3

                    )



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





            error_message = str(e)





            try:



                self.audit_engine.record(



                    task,



                    0.0,



                    1.0,



                    {


                        "decision":

                            "BLOCK",



                        "reason":

                            "Runtime Exception",



                        "error":

                            error_message



                    },



                    {


                        "status":

                            "FAILED",



                        "error":

                            error_message



                    }



                )



            except Exception:



                pass









            return {



                "execution_id":

                    execution_id,



                "execution_mode":

                    execution_mode,



                "task":

                    task,



                "agent":

                    agent or "RuntimeOrchestrator",



                "route":

                    "RuntimeFailureHandler",



                "decision":

                    "BLOCK",



                "trust_score":

                    0.0,



                "risk_score":

                    1.0,



                "conflict_score":

                    0.0,



                "model":

                    model or "unknown",



                "provider":

                    provider or "unknown",





                "routing":{


                    "strategy":

                        "FAIL_SAFE",



                    "selected":{


                        "model":

                            model or "unknown",



                        "provider":

                            provider or "unknown"



                    }



                },





                "result":{


                    "status":

                        "FAILED",



                    "error":

                        error_message



                },





                "cost":{


                    "cost_usd":

                        0,



                    "currency":

                        "USD"



                },





                "governance":{


                    "decision":

                        "BLOCK",



                    "reason":

                        "Runtime safety fallback"



                },





                "telemetry":{


                    "latency_ms":

                        round(

                            latency,

                            3

                        ),



                    "quality_score":

                        0



                },





                "runtime_ms":

                    round(

                        latency,

                        3

                    )



            }








# =====================================================
# GLOBAL INSTANCE
# =====================================================


orchestrator = RuntimeOrchestrator()



# =====================================================
# BACKWARD COMPATIBILITY
# =====================================================


Orchestrator = RuntimeOrchestrator