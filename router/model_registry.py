
class ModelRegistry:



    def __init__(self):


        self.models = [


            {

            "name":
            "gpt-5",


            "provider":
            "openai",


            "trust":
            95,


            "quality":
            95,


            "latency":
            800,


            "cost":
            0.02

            },


            {

            "name":
            "claude-sonnet-4",


            "provider":
            "anthropic",


            "trust":
            97,


            "quality":
            98,


            "latency":
            600,


            "cost":
            0.015

            },


            {

            "name":
            "llama-3-70b",


            "provider":
            "local",


            "trust":
            85,


            "quality":
            82,


            "latency":
            50,


            "cost":
            0

            }

        ]



    def get_models(self):

        return self.models