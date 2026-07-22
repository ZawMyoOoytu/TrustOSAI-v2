class CostEngine:


    MODEL_PRICING = {

        "gpt-4o": {

            "input":0.005,
            "output":0.015

        },


        "claude-3.5-sonnet":{

            "input":0.003,
            "output":0.015

        },


        "gemini-pro":{

            "input":0.0005,
            "output":0.0015

        },


        "local":{

            "input":0,
            "output":0

        }


    }



    def calculate(
        self,
        model="local",
        prompt_tokens=0,
        completion_tokens=0
    ):


        pricing = self.MODEL_PRICING.get(

            model,

            self.MODEL_PRICING["local"]

        )



        input_cost = (

            prompt_tokens / 1000

        ) * pricing["input"]



        output_cost = (

            completion_tokens / 1000

        ) * pricing["output"]




        total = (

            input_cost

            +

            output_cost

        )



        return {


            "cost_usd":

                round(total,6),


            "currency":

                "USD",


            "model":

                model,


            "tokens":

            {

                "input":

                    prompt_tokens,


                "output":

                    completion_tokens,


                "total":

                    prompt_tokens + completion_tokens

            }


        }