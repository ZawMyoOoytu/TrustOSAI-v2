class RouterEngine:



    def calculate_score(
        self,
        model
    ):


        score = (

            model["trust"] * 0.4

            +

            model["quality"] * 0.3

            +

            (100-model["latency"]/10)
            *0.2

            -

            model["cost"] * 10
            *0.1

        )


        return round(
            score,
            2
        )



    def select(
        self,
        models
    ):


        ranked=[]


        for model in models:


            score = self.calculate_score(
                model
            )


            ranked.append(

                {

                "model":model,

                "routing_score":
                score

                }

            )



        ranked.sort(

            key=lambda x:
            x["routing_score"],

            reverse=True

        )


        return ranked[0], ranked