class TrustExplanationEngine:


    def explain(
        self,
        execution
    ):


        factors = []


        # Model Reliability

        model_score = 80

        factors.append({

            "name":
            "Model Reliability",

            "score":
            model_score,

            "weight":
            0.30,

            "contribution":
            model_score * 0.30,

            "description":
            "Historical model execution stability"

        })



        # Risk Compliance

        risk_score = execution.risk_score


        compliance = max(
            0,
            100 - risk_score
        )


        factors.append({

            "name":
            "Policy Compliance",

            "score":
            compliance,

            "weight":
            0.30,

            "contribution":
            compliance * 0.30,

            "description":
            "Policy and safety evaluation"

        })



        # Historical Trust

        history = execution.trust_score


        factors.append({

            "name":
            "Historical Trust",

            "score":
            history,

            "weight":
            0.40,

            "contribution":
            history * 0.40,

            "description":
            "Previous execution behavior"

        })


        return {

            "execution_id":
            execution.id,


            "final_score":
            execution.trust_score,


            "level":
            self.level(
                execution.trust_score
            ),


            "factors":
            factors,


            "recommendation":
            self.recommendation(
                execution.decision
            )

        }



    def level(
        self,
        score
    ):

        if score >= 80:
            return "HIGH"

        if score >= 50:
            return "MEDIUM"

        return "LOW"



    def recommendation(
        self,
        decision
    ):

        mapping={

            "ALLOW":
            "Execute normally",

            "ALLOW_WITH_MONITORING":
            "Execute with continuous monitoring",

            "REVIEW":
            "Require human review",

            "BLOCK":
            "Execution prohibited"

        }


        return mapping.get(
            decision,
            "Unknown"
        )