from sqlalchemy.orm import Session
from typing import Dict, Any
import time


from database.repository import MetricsRepository



class TrustEngine:


    """
    TrustOSAI Adaptive Trust Evaluation Engine


    T(t)=

    [
       wr R(t)
      +ws S(t)
      +we E(t)

    ]*100

    - beta P(t)

    + alpha F(t)


    """



    def __init__(self):


        self.weights = {


            "reliability":

                0.45,


            "security":

                0.35,


            "efficiency":

                0.20

        }



        self.alpha = 0.15


        self.beta_penalty = 0.25


        self.critical_threshold = 60





    # =====================================================
    # NORMALIZATION
    # =====================================================

    def normalize_score(
        self,
        value,
        max_value=100
    ):


        try:

            value=float(value)


        except:

            return 0.0



        return min(

            max(

                value/max_value,

                0

            ),

            1

        )





    # =====================================================
    # TRUST EVALUATION
    # =====================================================

    def evaluate(
        self,
        task:str,
        db:Session,
        execution_id=None
    ):


        start_time=time.time()



        repo = MetricsRepository(db)



        logs = repo.get_recent_execution_logs(

            limit=20

        )





        if not logs:


            trust_score = 80.0



            return {


                "trust_score":

                    trust_score,


                "components":{


                    "reliability":

                        0.8,


                    "security":

                        0.85,


                    "efficiency":

                        0.85

                }


            }






        # =================================================
        # Reliability
        # =================================================


        reliability_values=[]



        for log in logs:


            score=getattr(

                log,

                "quality_score",

                None

            )



            if score is not None:


                reliability_values.append(

                    float(score)

                )



        if reliability_values:


            reliability=(

                sum(reliability_values)

                /

                len(reliability_values)

            )


        else:


            reliability=0.7





        reliability=max(

            reliability,

            0.5

        )





        # =================================================
        # Security
        # =================================================


        try:


            security=repo.get_policy_compliance_rate()



        except:


            security=0.85





        security=min(

            max(

                float(security),

                0.5

            ),

            1

        )






        # =================================================
        # Efficiency
        # =================================================


        try:


            efficiency=repo.get_cost_efficiency_index()



        except:


            efficiency=0.85





        efficiency=min(

            max(

                float(efficiency),

                0.5

            ),

            1

        )





        # =================================================
        # Failure Penalty
        # =================================================


        try:


            failure_rate=repo.get_failure_rate()



        except:


            failure_rate=0





        failure_rate=min(

            max(

                float(failure_rate),

                0

            ),

            1

        )





        # =================================================
        # Adaptive Trust Equation
        # =================================================


        feedback=reliability



        base=(


            self.weights["reliability"]

            *

            reliability



            +



            self.weights["security"]

            *

            security



            +



            self.weights["efficiency"]

            *

            efficiency

        )





        trust=(


            base


            -


            self.beta_penalty

            *

            failure_rate



            +



            self.alpha

            *

            feedback

        )




        trust_score=round(

            min(

                max(

                    trust*100,

                    0

                ),

                100

            ),

            2

        )





        latency_ms=round(

            (

                time.time()

                -

                start_time

            )

            *

            1000,

            3

        )





        return {


            "trust_score":

                trust_score,



            "components":{


                "reliability":

                    round(reliability,4),


                "security":

                    round(security,4),


                "efficiency":

                    round(efficiency,4),


                "failure_rate":

                    round(failure_rate,4)

            },



            "trace":{


                "execution_id":

                    execution_id,


                "engine":

                    "TrustEngine",


                "latency_ms":

                    latency_ms,


                "output":{


                    "trust_score":

                        trust_score,


                    "threshold":

                        self.critical_threshold

                }

            }

        }





    # =====================================================
    # TRUST MUTATION
    # =====================================================

    def mutate_trust_score(
        self,
        current_trust,
        feedback_quality
    ):


        current=float(current_trust)/100



        updated=(

            current

            +

            self.alpha

            *

            (

                feedback_quality-current

            )

        )



        return round(

            min(

                max(

                    updated*100,

                    0

                ),

                100

            ),

            2

        )





    # =====================================================
    # GOVERNANCE BOUNDS
    # =====================================================

    def evaluate_trust_bounds(
        self,
        request_data:Dict[str,Any],
        db:Session,
        execution_id=None
    ):


        result=self.evaluate(

            request_data.get(

                "task",

                ""

            ),

            db,

            execution_id

        )



        trust=result["trust_score"]





        if trust >=80:


            level="HIGH"



        elif trust>=60:


            level="MEDIUM"



        else:


            level="CRITICAL"





        return {


            "aggregated_trust":

                trust,


            "is_system_viable":

                trust>=self.critical_threshold,



            "target_bounds_level":

                level,



            "components":

                result["components"],



            "trace":

                result["trace"]

        }