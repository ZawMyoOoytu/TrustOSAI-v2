class PolicyEngine:


    def check(
        self,
        trust_score,
        risk_score
    ):


        if trust_score >= 0.75 and risk_score <= 0.5:

            return "ALLOW"


        return "BLOCK"