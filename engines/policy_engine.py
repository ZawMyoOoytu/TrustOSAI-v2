from typing import Dict, Any, Tuple
import time



class PolicyEngine:
    """
    TrustOSAI Policy Governance Engine v2.0

    Responsibilities:

    - Static Safety Enforcement
    - Trust Boundary Validation
    - Risk Constraint Validation
    - RBAC Authorization
    - Policy Trace Generation

    """



    def __init__(self):


        # ==========================================
        # Forbidden Policy Topics
        # ==========================================

        self.blacklisted_topics = [

            "classified_military_data",

            "unauthorized_financial_transfer",

            "root_credential_leak",

            "credential_extraction",

            "secret_key_dump"

        ]



        # ==========================================
        # Role Permission Model
        # ==========================================

        self.role_permissions = {


            "admin":

            [

                "read",

                "write",

                "execute",

                "override"

            ],



            "operator":

            [

                "read",

                "write",

                "execute"

            ],



            "user-default-01":

            [

                "read",

                "execute"

            ],



            # Runtime default user

            "guest":

            [

                "read",

                "execute"

            ]

        }



        # ==========================================
        # Governance Threshold
        # ==========================================


        self.minimum_trust = 50.0


        self.maximum_risk = 0.80



        self.policy_version = "v1.1.0"







    # ==========================================
    # Risk Normalization
    # ==========================================


    def normalize_risk(
        self,
        risk_score: float
    ) -> float:


        try:

            risk_score=float(
                risk_score or 0
            )

        except:

            risk_score=0.0



        # convert percentage

        if risk_score > 1:

            risk_score = risk_score / 100



        return min(

            max(

                risk_score,

                0.0

            ),

            1.0

        )







    # ==========================================
    # Legacy Interface
    # ==========================================


    def check(
        self,
        trust_score: float,
        risk_score: float
    ) -> str:



        trust_score=float(
            trust_score or 0
        )


        risk_score=self.normalize_risk(
            risk_score
        )



        if (

            trust_score < self.minimum_trust

            or

            risk_score > self.maximum_risk

        ):

            return "FAILED"



        return "PASSED"








    # ==========================================
    # Advanced Policy Constraint Engine
    # ==========================================


    def check_constraints(
        self,
        request_data: Dict[str,Any],
        execution_id=None
    ) -> Tuple[bool,Dict[str,Any]]:



        start_time=time.time()



        task=str(

            request_data.get(

                "task",

                ""

            )

        )



        task_content=task.lower()






        # Default runtime identity

        user_role=request_data.get(

            "user_role",

            "user-default-01"

        )




        trust_score=float(

            request_data.get(

                "trust_score",

                0

            )

        )




        risk_score=self.normalize_risk(

            request_data.get(

                "risk_score",

                0

            )

        )



        violations=[]






        # ==========================================
        # 1. Static Safety Policy
        # ==========================================


        for topic in self.blacklisted_topics:


            if topic in task_content:


                violations.append(

                    {

                        "type":

                            "STATIC_POLICY",


                        "message":

                            f"Forbidden topic detected: {topic}"

                    }

                )







        # ==========================================
        # 2. Trust Boundary
        # ==========================================


        if trust_score < self.minimum_trust:


            violations.append(

                {

                    "type":

                        "TRUST_THRESHOLD",


                    "message":

                        "Trust score below minimum governance threshold"

                }

            )








        # ==========================================
        # 3. Risk Boundary
        # ==========================================


        if risk_score > self.maximum_risk:


            violations.append(

                {

                    "type":

                        "RISK_THRESHOLD",


                    "message":

                        "Risk score exceeds maximum allowed level"

                }

            )








        # ==========================================
        # 4. RBAC Authorization
        # ==========================================


        required_permission="execute"



        mutation_actions=[


            "delete",

            "update",

            "modify",

            "write",

            "allocate"


        ]



        if any(

            action in task_content

            for action in mutation_actions

        ):


            required_permission="write"







        allowed_permissions=self.role_permissions.get(

            user_role,

            []

        )





        if required_permission not in allowed_permissions:


            violations.append(

                {


                    "type":

                        "RBAC_POLICY",



                    "message":

                        f"Role '{user_role}' lacks '{required_permission}' permission"


                }

            )








        # ==========================================
        # Policy Verdict
        # ==========================================


        policy_passed=(

            len(violations)==0

        )





        if policy_passed:


            governance_level="SAFE"


        elif len(violations)<=2:


            governance_level="REVIEW"


        else:


            governance_level="BLOCK"








        latency_ms=round(

            (time.time()-start_time)

            *

            1000,

            3

        )







        metadata={


            "execution_id":

                execution_id,



            "policy_passed":

                policy_passed,



            "policy_status":

                (

                    "APPROVED"

                    if policy_passed

                    else

                    "REJECTED"

                ),




            "governance_level":

                governance_level,



            "user_role":

                user_role,



            "required_permission":

                required_permission,



            "trust_score":

                trust_score,



            "risk_score":

                risk_score,



            "violations":

                violations,



            "rule_set_version":

                self.policy_version,





            "trace":

            {


                "engine":

                    "PolicyEngine",



                "execution_id":

                    execution_id,



                "latency_ms":

                    latency_ms,



                "output":

                {


                    "status":

                        (

                            "PASS"

                            if policy_passed

                            else

                            "FAILED"

                        ),



                    "governance_level":

                        governance_level,



                    "policy_version":

                        self.policy_version


                }


            }


        }





        return (

            policy_passed,

            metadata

        )