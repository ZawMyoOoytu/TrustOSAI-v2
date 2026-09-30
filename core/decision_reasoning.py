class DecisionReasoningEngine:


    def generate(self, execution):


        reasoning=[]

        actions=[]



        trust = execution.trust_score

        risk = execution.risk_score

        decision = execution.decision




        # Trust evaluation

        if trust >= 80:

            reasoning.append(
                "High trust score indicates reliable execution"
            )


        elif trust >= 50:

            reasoning.append(
                "Trust score is moderate and requires monitoring"
            )


        else:

            reasoning.append(
                "Low trust score requires additional control"
            )





        # Risk evaluation

        if risk == 0:

            reasoning.append(
                "Risk score is within acceptable range"
            )

        else:

            reasoning.append(
                f"Risk detected with score {risk}"
            )







        # Decision explanation


        if decision == "ALLOW":


            actions.extend([

                "Execute agent normally",

                "Store execution audit"

            ])




        elif decision == "ALLOW_WITH_MONITORING":


            reasoning.append(
                "Continuous monitoring policy activated"
            )


            actions.extend([

                "Execute agent",

                "Monitor runtime behavior",

                "Store audit record"

            ])





        elif decision == "REVIEW":


            actions.extend([

                "Pause execution",

                "Request human review"

            ])





        elif decision == "BLOCK":


            actions.extend([

                "Prevent execution",

                "Record security event"

            ])




        return {


            "execution_id":
            execution.id,


            "decision":
            decision,


            "reasoning":
            reasoning,


            "actions":
            actions,


            "confidence":
            round(
                trust / 100,
                2
            )


        }