class ReplayAnalyzer:


    def analyze(
        self,
        original,
        replay
    ):


        trust_delta = (
            replay.trust_score
            -
            original.trust_score
        )


        decision_changed = (
            original.decision
            !=
            replay.decision
        )


        risk_changed = (
            original.risk_score
            !=
            replay.risk_score
        )


        if abs(trust_delta) < 5:
            stability = "HIGH"

        elif abs(trust_delta) < 15:
            stability = "MEDIUM"

        else:
            stability = "LOW"



        return {


            "trust_drift": {

                "original":
                    original.trust_score,

                "replay":
                    replay.trust_score,

                "delta":
                    round(
                        trust_delta,
                        2
                    )

            },


            "decision_analysis": {


                "original":
                    original.decision,


                "replay":
                    replay.decision,


                "changed":
                    decision_changed

            },


            "risk_analysis": {


                "original":
                    original.risk_score,


                "replay":
                    replay.risk_score,


                "changed":
                    risk_changed

            },


            "stability":
                stability

        }