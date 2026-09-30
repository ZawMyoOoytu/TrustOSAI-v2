from typing import Dict, Any
from datetime import datetime


from engines.providers.local_provider import LocalProvider



class ModelRouter:

    """
    =====================================================
    TrustOSAI Adaptive Model Router v2.1
    =====================================================

    Responsible for:

    - Provider selection
    - Model routing
    - Fallback
    - Runtime metadata
    - Cost tracking
    - Telemetry propagation

    =====================================================
    """



    def __init__(self):


        self.providers = {


            "local":

                LocalProvider()

        }



        self.default_provider = "local"






    # =====================================================
    # REGISTER PROVIDER
    # =====================================================


    def register_provider(

        self,

        name:str,

        provider

    ):


        self.providers[

            name.lower()

        ] = provider






    # =====================================================
    # AVAILABLE PROVIDERS
    # =====================================================


    def available_providers(self):


        return list(

            self.providers.keys()

        )







    # =====================================================
    # ROUTE MODEL
    # =====================================================


    def select_provider(

        self,

        provider:str | None

    ):



        if provider:


            provider = provider.lower()



            if provider in self.providers:


                return provider





        return self.default_provider







    # =====================================================
    # EXECUTE MODEL
    # =====================================================


    def execute(


        self,


        task:str,


        model:str="local",


        provider:str="local",


        api_key=None



    ) -> Dict[str,Any]:



        start=datetime.utcnow()



        selected_provider = self.select_provider(

            provider

        )




        router_provider = self.providers.get(

            selected_provider

        )





        fallback=False




        # ==========================================
        # FALLBACK
        # ==========================================


        if router_provider is None:


            router_provider = self.providers[

                self.default_provider

            ]


            selected_provider = self.default_provider


            fallback=True





        # ==========================================
        # EXECUTION
        # ==========================================


        try:



            response = router_provider.generate(


                task,


                model=model,


                api_key=api_key


            )





        except Exception as e:



            return {


                "status":"FAILED",


                "error":str(e),



                "router":{


                    "provider":

                        selected_provider,


                    "model":

                        model,


                    "fallback":

                        fallback

                }


            }







        if not isinstance(response,dict):


            response={

                "response":

                    str(response)

            }







        # ==========================================
        # TELEMETRY
        # ==========================================



        end=datetime.utcnow()



        runtime_ms=(

            end-start

        ).total_seconds()*1000







        response.update({



            "model":model,


            "provider":selected_provider,



            "telemetry":{


                "runtime_ms":

                    runtime_ms,


                "timestamp":

                    end.isoformat()



            },



            "router_metadata":{


                "requested_model":

                    model,


                "selected_provider":

                    selected_provider,


                "fallback_used":

                    fallback



            }



        })






        return response