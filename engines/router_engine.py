from typing import Dict, Any


class RouterEngine:
    """
    TrustOSAI Intelligent Model Routing Engine

    Selects optimal execution agent based on:

    Utility(m)=
        Accuracy
        - Cost
        - Latency

    """


    def __init__(self):


        self.agent_pool = {


            "gpt-4o": {


                "model_name":
                    "gpt-4o",


                "cost":
                    0.015,


                "latency":
                    1.2,


                "accuracy":
                    0.95,


                "capabilities":

                [
                    "reasoning",
                    "coding",
                    "analysis"
                ]

            },



            "llama-3-70b": {


                "model_name":
                    "llama-3-70b",


                "cost":
                    0.002,


                "latency":
                    0.8,


                "accuracy":
                    0.85,


                "capabilities":

                [
                    "text",
                    "summary"
                ]

            },



            "phi-3-mini": {


                "model_name":
                    "phi-3-mini",


                "cost":
                    0.0001,


                "latency":
                    0.3,


                "accuracy":
                    0.65,


                "capabilities":

                [
                    "classification"
                ]

            }

        }




    # =================================================
    # Legacy Route
    # =================================================

    def route(
        self,
        task:str
    ):

        return self.select_optimal_agent(

            {
                "aggregated_trust":100
            },

            {
                "task":task
            }

        )




    # =================================================
    # Optimization Router
    # =================================================

    def select_optimal_agent(
        self,
        trust_context:Dict[str,Any],
        request_data:Dict[str,Any]
    ):


        trust = trust_context.get(

            "aggregated_trust",

            100

        )


        task = request_data.get(

            "task",

            ""

        ).lower()



        if trust < 70:


            w_accuracy=0.7

            w_cost=0.2

            w_latency=0.1


        else:


            w_accuracy=0.4

            w_cost=0.4

            w_latency=0.2




        best=None

        best_score=-999



        for name,model in self.agent_pool.items():


            capability_bonus=0.0


            for cap in model["capabilities"]:

                if cap in task:

                    capability_bonus=0.1



            score=(

                w_accuracy *
                (
                    model["accuracy"]
                    +
                    capability_bonus
                )

                -

                w_cost *
                (
                    model["cost"]/0.015
                )

                -

                w_latency *
                (
                    model["latency"]/1.2
                )

            )



            if score > best_score:


                best_score=score

                best=model["model_name"]



        return best