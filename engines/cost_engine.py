from typing import Dict,Any



class CostEngine:


    def __init__(self):


        self.pricing={


            "gpt-4o":
            {

                "input":5.0,

                "output":15.0

            },


            "llama-3-70b":
            {

                "input":0.59,

                "output":0.79

            },


            "phi-3-mini":
            {

                "input":0.05,

                "output":0.10

            }

        }





    def calculate(
        self,
        task:str,
        model="gpt-4o"
    )->Dict[str,Any]:



        input_tokens=max(

            len(task.split()),

            1

        )


        output_tokens=10



        price=self.pricing.get(

            model,

            self.pricing["gpt-4o"]

        )



        input_cost=(

            input_tokens
            /
            1_000_000

        )*price["input"]



        output_cost=(

            output_tokens
            /
            1_000_000

        )*price["output"]




        return {


            "model":
                model,


            "input_tokens":
                input_tokens,


            "output_tokens":
                output_tokens,


            "total_cost":

                round(

                    input_cost+output_cost,

                    8

                )

        }