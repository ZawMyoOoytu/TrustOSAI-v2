from sqlalchemy.orm import Session
from typing import Dict, Any, Tuple
import time


from engines.trust_engine import TrustEngine
from engines.risk_engine import RiskEngine
from engines.policy_engine import PolicyEngine
from engines.conflict_engine import ConflictEngine



class GovernanceEngine:
    """
    TrustOSAI Adaptive Governance Engine v2.1


    Decision Model:

    Security Violation
            |
            BLOCK


    Risk > threshold
            |
            BLOCK


    Conflict
            |
            BLOCK


    Trust:

        >=80
            ALLOW

        60-80
            ALLOW_WITH_MONITORING

        40-60
            REVIEW

        <40
            BLOCK

    """



    def __init__(self):

        self.trust_engine = TrustEngine()

        self.risk_engine = RiskEngine()

        self.policy_engine = PolicyEngine()

        self.conflict_engine = ConflictEngine()



        self.high_trust = 80.0

        self.medium_trust = 60.0

        self.low_trust = 40.0


        self.max_allowable_risk = 0.70





    # =====================================================
    # Legacy Interface
    # =====================================================

    def evaluate(
        self,
        trust_score: float,
        risk_score: float,
        policy: str,
        conflict: bool,
        context=None
    ) -> Dict[str, Any]:


        if conflict:

            return {

                "status":"BLOCK",

                "reason":"Conflict detected"

            }



        if risk_score > self.max_allowable_risk:

            return {

                "status":"BLOCK",

                "reason":"Risk threshold exceeded"

            }



        if trust_score < self.low_trust:

            return {

                "status":"BLOCK",

                "reason":"Trust critically low"

            }



        return {

            "status":"ALLOW",

            "reason":"Governance passed"

        }







    # =====================================================
    # Main Governance Pipeline
    # =====================================================


    def evaluate_request(
        self,
        request_data: Dict[str,Any],
        db: Session,
        execution_id=None
    ) -> Tuple[str,Dict[str,Any]]:


        start=time.time()


        trace=[]





        # =================================================
        # Trust Evaluation
        # =================================================


        trust_context = (

            self.trust_engine
            .evaluate_trust_bounds(

                request_data,

                db,

                execution_id

            )

        )



        trust_score=float(

            trust_context.get(

                "aggregated_trust",

                0

            )

        )



        trace.append({

            "engine":

                "TrustEngine",

            "output":

                trust_score

        })







        # =================================================
        # Risk Evaluation
        # =================================================


        _, risk_score, risk_metadata = (

            self.risk_engine
            .analyze_intent(

                request_data

            )

        )


        risk_score=float(risk_score)



        trace.append({

            "engine":

                "RiskEngine",

            "output":

                risk_score

        })







        # =================================================
        # Policy Evaluation
        # IMPORTANT:
        # Pass Trust + Risk to Policy Engine
        # =================================================


        policy_request = {


            **request_data,


            "trust_score":

                trust_score,


            "risk_score":

                risk_score


        }



        policy_passed, policy_metadata = (

            self.policy_engine
            .check_constraints(

                policy_request,

                execution_id

            )

        )



        trace.append({

            "engine":

                "PolicyEngine",


            "output":

                (

                    "PASS"

                    if policy_passed

                    else

                    "FAILED"

                )

        })







        # =================================================
        # Conflict Detection
        # =================================================


        has_conflict, conflict_metadata = (

            self.conflict_engine
            .check_concurrency(

                request_data,

                db

            )

        )



        conflict_score = (

            1.0

            if has_conflict

            else

            0.0

        )



        trace.append({

            "engine":

                "ConflictEngine",


            "output":

                (

                    "CONFLICT"

                    if has_conflict

                    else

                    "CLEAR"

                )

        })







        # =================================================
        # Governance Decision
        # =================================================


        decision="ALLOW"

        reason=""

        details={}





        # Hard Security Controls


        if not policy_passed:


            decision="BLOCK"


            reason="Policy violation"


            details = policy_metadata.get(

                "violations",

                []

            )



        elif risk_score > self.max_allowable_risk:


            decision="BLOCK"


            reason="Risk threshold exceeded"


            details=risk_metadata





        elif has_conflict:


            decision="BLOCK"


            reason="Execution conflict"


            details=conflict_metadata





        # Adaptive Trust Layer


        elif trust_score < self.low_trust:


            decision="BLOCK"


            reason="Trust critically low"





        elif trust_score < self.medium_trust:


            decision="REVIEW"


            reason="Human review recommended"





        elif trust_score < self.high_trust:


            decision="ALLOW_WITH_MONITORING"


            reason="Moderate trust"





        else:


            decision="ALLOW"


            reason="High trust"






        trace.append({

            "engine":

                "GovernanceDecision",


            "output":

                decision

        })







        latency_ms = round(

            (time.time()-start)*1000,

            3

        )







        metadata={


            "execution_id":

                execution_id,


            "trust_score":

                trust_score,


            "risk_score":

                risk_score,


            "conflict_score":

                conflict_score,


            "decision":

                decision,


            "reason":

                reason,


            "details":

                details,



            "trust_context":

                trust_context,



            "trace":

                trace,



            "latency_ms":

                latency_ms,



            "sub_engines":


            {


                "risk":

                    risk_metadata,


                "policy":

                    policy_metadata,


                "conflict":

                    conflict_metadata


            }


        }



        return decision, metadata