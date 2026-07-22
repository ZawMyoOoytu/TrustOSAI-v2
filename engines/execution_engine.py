import time

from datetime import datetime

from typing import Dict, Any


from engines.model_router import ModelRouter





class ExecutionEngine:


    """
    =====================================================
    TrustOSAI Runtime Execution Engine v4.0
    =====================================================


    Enterprise Execution Layer


    Responsibilities:

    - Model execution abstraction
    - Provider routing
    - BYOK API key propagation
    - Token telemetry
    - Quality measurement
    - Runtime trace
    - Replay compatibility


    Pipeline:


        RouterEngine

             |

             v


        ExecutionEngine

             |

             v


        ModelRouter


             |

    -------------------

    Local LLM

    OpenAI

    Gemini

    Ollama

    vLLM

    -------------------


    """





    # =====================================================
    # INIT
    # =====================================================


    def __init__(self):


        self.model_router = ModelRouter()



        self.model_profiles = {



            "gpt-4o":

            {

                "provider":

                    "openai",


                "quality":

                    0.92

            },




            "llama-3-70b":

            {

                "provider":

                    "local",


                "quality":

                    0.82

            },




            "phi-3-mini":

            {

                "provider":

                    "local",


                "quality":

                    0.68

            },




            "local":

            {

                "provider":

                    "local",


                "quality":

                    0.75

            }


        }








    # =====================================================
    # LEGACY SUPPORT
    # =====================================================


    def run(

        self,

        task:str

    ):



        result = self.execute(


            routed_model="local",


            task=task


        )



        return result.get(

            "response",

            ""

        )









    # =====================================================
    # MAIN EXECUTION
    # =====================================================


    def execute(


        self,


        routed_model=None,


        task=None,


        execution_id=None,


        api_key=None,


        model=None,


        provider=None


    ) -> Dict[str,Any]:



        start_time = time.perf_counter()





        try:




            # =================================================
            # MODEL RESOLUTION
            # =================================================



            selected_model = (


                model

                or

                routed_model

                or

                "local"

            )




            profile = self.model_profiles.get(


                selected_model,


                self.model_profiles["local"]

            )




            selected_provider = (


                provider

                or

                profile.get(

                    "provider",

                    "local"

                )

            )









            # =================================================
            # MODEL ROUTER EXECUTION
            # =================================================



            model_result = self.model_router.execute(


                model=selected_model,


                task=task,


                provider=selected_provider,


                api_key=api_key


            )






            if not isinstance(model_result,dict):


                model_result={

                    "response":

                        str(model_result)

                }









            response_text = model_result.get(


                "response",


                "Execution completed"


            )








            # =================================================
            # LATENCY
            # =================================================



            latency_ms = round(


                (

                    time.perf_counter()

                    -

                    start_time

                )

                *

                1000,


                3


            )









            # =================================================
            # TOKEN TELEMETRY
            # =================================================



            token_data = model_result.get(


                "token_telemetry",


                {}

            )




            if not isinstance(token_data,dict):


                token_data={}






            prompt_tokens = int(


                token_data.get(

                    "prompt_tokens",

                    len(task.split()) if task else 0

                )

            )





            completion_tokens = int(


                token_data.get(

                    "completion_tokens",

                    len(response_text.split())

                )

            )






            total_tokens = (


                prompt_tokens

                +

                completion_tokens

            )









            token_data.update({



                "prompt_tokens":

                    prompt_tokens,



                "completion_tokens":

                    completion_tokens,



                "total_tokens":

                    total_tokens,



                "context_window":

                    token_data.get(

                        "context_window",

                        8000

                    )

            })









            # =================================================
            # QUALITY
            # =================================================



            quality_score = float(


                model_result.get(


                    "quality_score",


                    profile["quality"]


                )

            )









            # =================================================
            # FINAL RESULT
            # =================================================



            result = {



                "response":


                    f"[{selected_model}] {response_text}",




                "model":

                    selected_model,




                "provider":

                    selected_provider,




                "quality_score_qt":

                    quality_score,




                "token_telemetry":

                    token_data,




                "status":

                    "COMPLETED",




                "runtime_ms":

                    latency_ms


            }









            # =================================================
            # TRACE
            # =================================================



            result["trace"] = {



                "execution_id":

                    execution_id,



                "engine":

                    "ExecutionEngine",



                "timestamp":

                    datetime.utcnow().isoformat(),




                "input":

                    task,




                "output":

                {



                    "model":

                        selected_model,



                    "provider":

                        selected_provider,



                    "quality_score":

                        quality_score,



                    "status":

                        "COMPLETED"

                }



            }








            return result







        # =====================================================
        # FAILURE
        # =====================================================


        except Exception as e:



            latency_ms = round(


                (

                    time.perf_counter()

                    -

                    start_time

                )

                *

                1000,


                3

            )




            return {



                "response":

                    "Execution failed",




                "model":

                    model or routed_model,




                "provider":

                    provider or "local",




                "quality_score_qt":

                    0.0,




                "token_telemetry":

                {



                    "prompt_tokens":

                        0,



                    "completion_tokens":

                        0,



                    "total_tokens":

                        0

                },




                "status":

                    "FAILED",




                "error":

                    str(e),




                "runtime_ms":

                    latency_ms,




                "trace":

                {



                    "execution_id":

                        execution_id,



                    "engine":

                        "ExecutionEngine",



                    "timestamp":

                        datetime.utcnow().isoformat(),



                    "status":

                        "FAILED"

                }

            }