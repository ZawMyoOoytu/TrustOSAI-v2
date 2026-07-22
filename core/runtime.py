import time

from typing import Dict, Any, Optional

from core.orchestrator import RuntimeOrchestrator




# =====================================================
# TRUSTOSAI RUNTIME KERNEL
# =====================================================


class TrustOSRuntime:
    """
    TrustOSAI Runtime Kernel v2.3


    Responsibilities:

    - Execute Runtime Orchestration
    - Propagate Agent Identity
    - Propagate Model Routing
    - Attach Runtime Telemetry
    - Normalize Execution Output
    - Protect Kernel Stability


    Pipeline:


        API

         |

         v

        ExecutionService

         |

         v

        TrustOSRuntime

         |

         v

        RuntimeOrchestrator

         |

         v

        Governance Pipeline



    """



    def __init__(self):

        self.orchestrator = RuntimeOrchestrator()





    # =====================================================
    # EXECUTION ENTRY POINT
    # =====================================================


    def execute(

        self,

        task: str,

        db=None,

        execution_id: Optional[int] = None,

        agent: Optional[str] = None,

        model: Optional[str] = None,

        provider: Optional[str] = None

    ) -> Dict[str, Any]:




        start = time.perf_counter()





        # =================================================
        # RUNTIME CONTEXT
        # =================================================


        runtime_context = {


            "execution_id": execution_id,


            "agent": agent,


            "model": model,


            "provider": provider


        }





        try:



            # =============================================
            # CALL ORCHESTRATOR
            # =============================================


            result = self.orchestrator.execute(


                task,


                db,


                execution_id=execution_id,


                agent=agent,


                model=model,


                provider=provider


            )





            # =============================================
            # VALIDATE RESULT
            # =============================================


            if not isinstance(
                result,
                dict
            ):


                result = {


                    "decision":
                        "BLOCK",


                    "result":
                        "Invalid orchestrator response"


                }





        except TypeError:



            """
            Backward compatibility

            If old RuntimeOrchestrator
            does not accept new parameters
            """



            try:


                result = self.orchestrator.execute(

                    task,

                    db,

                    execution_id=execution_id

                )



            except Exception as e:


                return self.runtime_error(

                    task,

                    execution_id,

                    e,

                    start

                )





        except Exception as e:


            return self.runtime_error(

                task,

                execution_id,

                e,

                start

            )






        # =================================================
        # LATENCY
        # =================================================


        latency = (

            time.perf_counter()

            -

            start

        ) * 1000






        # =================================================
        # NORMALIZE OUTPUT
        # =================================================


        result.setdefault(

            "task",

            task

        )



        result.setdefault(

            "execution_id",

            execution_id

        )



        result.setdefault(

            "agent",

            agent

        )



        result.setdefault(

            "model",

            model

        )



        result.setdefault(

            "provider",

            provider

        )



        result.setdefault(

            "decision",

            "BLOCK"

        )



        result.setdefault(

            "trust_score",

            0.0

        )



        result.setdefault(

            "risk_score",

            0.0

        )



        result.setdefault(

            "conflict_score",

            0.0

        )






        # =================================================
        # TELEMETRY
        # =================================================


        telemetry = result.setdefault(

            "telemetry",

            {}

        )



        if not isinstance(
            telemetry,
            dict
        ):

            telemetry = {}

            result["telemetry"] = telemetry





        telemetry.update({


            "runtime_latency_ms":
                round(
                    latency,
                    3
                ),


            "agent":
                agent,


            "model":
                model,


            "provider":
                provider



        })





        result["runtime_ms"] = round(

            latency,

            3

        )






        # =================================================
        # RETURN FINAL RUNTIME RESULT
        # =================================================


        return result










    # =====================================================
    # ERROR HANDLER
    # =====================================================


    def runtime_error(

        self,

        task,

        execution_id,

        error,

        start

    ):



        latency = (

            time.perf_counter()

            -

            start

        ) * 1000




        return {


            "task":
                task,


            "execution_id":
                execution_id,


            "decision":
                "BLOCK",


            "trust_score":
                0.0,


            "risk_score":
                100.0,


            "conflict_score":
                0.0,



            "result": {


                "error":
                    str(error)


            },



            "telemetry": {


                "latency_ms":
                    round(
                        latency,
                        3
                    ),


                "quality_score":
                    0.0


            },



            "runtime_ms":
                round(
                    latency,
                    3
                )


        }