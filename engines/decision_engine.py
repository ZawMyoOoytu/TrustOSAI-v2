import time



class DecisionEngine:

    """
    TrustOSAI Governance Decision Engine


    Mathematical Model:

        D(t)=f(T,R,C)


    T = Trust Score
    R = Risk Score
    C = Conflict Score


    Output:

        APPROVED
        REVIEW
        BLOCK

    """



    def __init__(self):


        self.trust_threshold_high = 80

        self.trust_threshold_medium = 50


        self.risk_threshold_high = 75

        self.risk_threshold_medium = 40


        self.conflict_threshold = 50



        self.last_trace = None





    # =====================================================
    # Normalize Input
    # =====================================================

    def normalize_score(self,value):


        try:

            return float(value or 0)


        except Exception:

            return 0.0





    # =====================================================
    # Decision Function
    # =====================================================

    def decide(
        self,
        trust,
        risk,
        conflict,
        execution_id=None
    ):


        start=time.time()



        trust=self.normalize_score(
            trust
        )


        risk=self.normalize_score(
            risk
        )


        conflict=self.normalize_score(
            conflict
        )




        # Convert normalized values

        if risk <= 1:

            risk*=100



        if conflict <=1:

            conflict*=100





        # =================================================
        # Governance Policy
        # =================================================


        if risk >= self.risk_threshold_high:


            decision="BLOCK"



        elif conflict >= self.conflict_threshold:


            decision="REVIEW"



        elif (

            trust >= self.trust_threshold_high

            and

            risk < self.risk_threshold_medium

            and

            conflict == 0

        ):


            decision="APPROVED"



        elif trust >= self.trust_threshold_medium:


            decision="REVIEW"



        else:


            decision="BLOCK"





        latency_ms=round(

            (time.time()-start)*1000,

            3

        )




        self.last_trace={


            "execution_id":

                execution_id,


            "engine":

                "DecisionEngine",


            "latency_ms":

                latency_ms,


            "input":

            {

                "trust":

                    trust,


                "risk":

                    risk,


                "conflict":

                    conflict

            },


            "decision":

                decision

        }





        return decision





    # =====================================================
    # Trace Access
    # =====================================================


    def get_trace(self):

        return self.last_trace