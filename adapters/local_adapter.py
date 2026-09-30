import time

from .base_adapter import BaseModelAdapter



class LocalModelAdapter(
    BaseModelAdapter
):


    def execute(
        self,
        prompt,
        model,
        **kwargs
    ):


        start=time.time()


        response = {

            "response":
            f"[{model}] [LOCAL RUNTIME] AI execution completed.",


            "model":
            model,


            "provider":
            "local",


            "status":
            "COMPLETED"

        }


        response["runtime_ms"] = (
            time.time()-start
        ) * 1000


        return response