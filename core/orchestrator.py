import time

from typing import Dict, Any
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
    TrustOSAI Adaptive Execution Orchestrator v2.3


    Execution Pipeline:

        Request

           |

           v

        Memory Context

           |

           v

        Governance Engine

           |

           v

        Agent Router

           |

           v

        Execution Engine

           |

           v

        Cost Engine

           |

           v

        Telemetry

           |

           v

        Audit + Memory Feedback


    Execution Identity Flow:

        execution_id

              |

              v

        Runtime

              |

              v

        ExecutionEngine

              |

              v

        Trace


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
        user_role: str = "user-default-01"
    ) -> Dict[str, Any]:


        start_time = time.perf_counter()



        try:


            # =================================================
            # 1. MEMORY
            # =================================================


            context = self.memory_engine.retrieve_context(

                task,

                db

            )



            request_data = {

                "task": task,

                "context": context,

                "user_role": user_role

            }




            # =================================================
            # 2. GOVERNANCE
            # =================================================


            decision, governance = (

                self.governance_engine.evaluate_request(

                    request_data,

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
            # 3. BLOCK
            # =================================================


            if decision == "BLOCK":


                latency = (

                    time.perf_counter()

                    - start_time

                ) * 1000



                blocked_response = {


                    "execution_id":

                        execution_id,


                    "decision":

                        "BLOCK",


                    "task":

                        task,


                    "trust_score":

                        trust_score,


                    "risk_score":

                        risk_score,


                    "conflict_score":

                        conflict_score,


                    "route":

                        "GovernanceAgent",


                    "result":

                    {

                        "status":

                            "BLOCKED",


                        "message":

                            "Execution blocked by governance policy"

                    },


                    "cost":

                    {

                        "cost_usd":

                            0.0

                    },


                    "governance":

                        governance,


                    "telemetry":

                    {

                        "latency_ms":

                            round(latency,3),


                        "quality_score":

                            0.0

                    }

                }



                self.audit_engine.record(

                    task,

                    trust_score,

                    risk_score,

                    governance,

                    blocked_response

                )



                return blocked_response





            # =================================================
            # 4. ROUTING
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

                        task

                }

            )






            # =================================================
            # 5. EXECUTION ENGINE
            # =================================================


            execution_result = (

                self.execution_engine.execute(

                    route,

                    task,

                    execution_id=execution_id

                )

            )







            # =================================================
            # 6. COST
            # =================================================


            raw_cost = self.cost_engine.calculate(

                task

            )


            if isinstance(raw_cost, dict):

                cost_usd = float(

                    raw_cost.get(

                        "cost_usd",

                        0

                    )

                )

            else:

                cost_usd = float(

                    raw_cost or 0

                )



            cost = {

                "cost_usd":

                    cost_usd

            }





            # =================================================
            # 7. TELEMETRY
            # =================================================


            telemetry = self.telemetry_engine.collect(

                task,

                {

                    "agent":

                        route,


                    "trust_score":

                        trust_score,


                    "risk_score":

                        risk_score,


                    "decision":

                        decision

                }

            )



            latency = (

                time.perf_counter()

                - start_time

            ) * 1000



            quality_score = float(

                telemetry.get(

                    "quality_score",

                    execution_result.get(

                        "quality_score_qt",

                        1.0

                    )

                )

            )





            # =================================================
            # 8. MEMORY UPDATE
            # =================================================


            self.memory_engine.update_memory(

                db,

                task,

                execution_result,

                quality_score

            )





            # =================================================
            # 9. AUDIT
            # =================================================


            self.audit_engine.record(

                task,

                trust_score,

                risk_score,

                governance,

                execution_result

            )







            # =================================================
            # FINAL RESPONSE
            # =================================================


            return {


                "execution_id":

                    execution_id,


                "decision":

                    decision,


                "task":

                    task,


                "trust_score":

                    trust_score,


                "risk_score":

                    risk_score,


                "conflict_score":

                    conflict_score,


                "route":

                    route,


                "result":

                    execution_result,


                "cost":

                    cost,


                "governance":

                    governance,


                "telemetry":

                {

                    "latency_ms":

                        round(latency,3),


                    "quality_score":

                        quality_score

                },


                "runtime_ms":

                    round(latency,3)

            }






        except Exception as e:


            latency = (

                time.perf_counter()

                - start_time

            ) * 1000



            return {


                "execution_id":

                    execution_id,


                "decision":

                    "BLOCK",


                "task":

                    task,


                "trust_score":

                    0.0,


                "risk_score":

                    1.0,


                "conflict_score":

                    0.0,


                "route":

                    "RuntimeOrchestrator",


                "result":

                {

                    "error":

                        str(e)

                },


                "cost":

                {

                    "cost_usd":

                        0.0

                },


                "telemetry":

                {

                    "latency_ms":

                        round(latency,3),


                    "quality_score":

                        0.0

                }

            }