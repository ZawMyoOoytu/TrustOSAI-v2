from .base_provider import BaseProvider



class LocalProvider(BaseProvider):


    def generate(
        self,
        task:str,
        **kwargs
    ):


        return {

            "response":
            "[LOCAL RUNTIME] "
            "AI execution completed.",


            "model":
            "local-runtime",


            "token_telemetry":
            {

                "prompt_tokens":
                len(task.split()),


                "completion_tokens":
                10

            },


            "status":
            "COMPLETED"

        }