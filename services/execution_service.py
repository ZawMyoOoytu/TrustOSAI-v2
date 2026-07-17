from datetime import datetime

from sqlalchemy.orm import Session


from engines.trust_engine import TrustEngine
from engines.risk_engine import RiskEngine
from engines.conflict_engine import ConflictEngine
from engines.policy_engine import PolicyEngine
from engines.decision_engine import DecisionEngine
from engines.telemetry_engine import TelemetryEngine
from engines.cost_engine import CostEngine


from database.models import Execution





class ExecutionService:


    """
    TrustOSAI Execution Control Plane


    Pipeline:

    API Request

        |

        v

    Execution Service

        |

        +--> Trust Engine

        +--> Risk Engine

        +--> Policy Engine

        +--> Conflict Engine

        +--> Decision Engine

        +--> Telemetry Engine

        +--> Cost Engine

        |

        v

    PostgreSQL Execution Ledger


    """




    def __init__(self):


        self.trust_engine = TrustEngine()

        self.risk_engine = RiskEngine()

        self.policy_engine = PolicyEngine()

        self.conflict_engine = ConflictEngine()

        self.decision_engine = DecisionEngine()

        self.telemetry_engine = TelemetryEngine()

        self.cost_engine = CostEngine()






    def execute(
        self,
        task: str,
        db: Session
    ):



        start_time = datetime.utcnow()



        # =====================================================
        # 1. TRUST ENGINE
        # =====================================================


        trust_result = self.trust_engine.evaluate(

            task,

            db

        )



        if isinstance(trust_result, dict):

            trust_score = trust_result.get(

                "trust_score",

                0

            )

        else:

            trust_score = trust_result



        trust_score = float(

            trust_score or 0

        )







        # =====================================================
        # 2. RISK ENGINE
        # =====================================================


        risk_result = self.risk_engine.analyze(

            task

        )



        if isinstance(risk_result, tuple):

            risk_score = risk_result[1]


        elif isinstance(risk_result, dict):

            risk_score = risk_result.get(

                "risk_score",

                0

            )


        else:

            risk_score = risk_result



        risk_score = float(

            risk_score or 0

        )



        # Convert normalized risk

        # 0.0-1.0 --> 0-100

        if risk_score <= 1:

            risk_percent = (

                risk_score * 100

            )

        else:

            risk_percent = risk_score







        # =====================================================
        # 3. POLICY ENGINE
        # =====================================================


        policy_passed, policy_metadata = (

            self.policy_engine.check_constraints(

                {

                    "task": task,

                    "trust_score": trust_score,

                    "risk_score": risk_percent

                }

            )

        )







        # =====================================================
        # 4. CONFLICT ENGINE
        # =====================================================


        conflict_result = self.conflict_engine.detect(

            task,

            policy_metadata,

            db

        )



        if isinstance(conflict_result, dict):

            conflict_score = conflict_result.get(

                "conflict_score",

                0

            )


        else:

            conflict_score = conflict_result



        conflict_score = float(

            conflict_score or 0

        )








        # =====================================================
        # 5. GOVERNANCE DECISION
        # =====================================================


        if not policy_passed:


            # Hard block only unsafe policy violation

            if risk_percent >= 75:


                decision = "BLOCK"


            else:


                decision = self.decision_engine.decide(

                    trust_score,

                    risk_percent,

                    conflict_score

                )


        else:


            decision = self.decision_engine.decide(

                trust_score,

                risk_percent,

                conflict_score

            )








        # =====================================================
        # 6. EXECUTION RESULT
        # =====================================================


        if decision == "APPROVED":


            result = (

                "Execution completed successfully"

            )


        elif decision == "REVIEW":


            result = (

                "Execution pending human governance review"

            )


        else:


            result = (

                "Execution blocked by governance policy"

            )








        # =====================================================
        # 7. RUNTIME METRICS
        # =====================================================


        end_time = datetime.utcnow()



        latency_ms = int(

            (

                end_time - start_time

            )

            .total_seconds()

            *

            1000

        )




        quality_score = round(

            trust_score / 100,

            4

        )









        # =====================================================
        # 8. COST ENGINE
        # =====================================================


        prompt_tokens = len(

            task.split()

        )


        completion_tokens = 3



        try:


            _, total_cost, cost_metadata = (

                self.cost_engine.calculate_financial_metrics(

                    "gpt-4o",

                    prompt_tokens,

                    completion_tokens

                )

            )


        except Exception:


            total_cost = 0

            cost_metadata = {}










        # =====================================================
        # 9. TELEMETRY ENGINE
        # =====================================================


        telemetry = self.telemetry_engine.collect(

            task,

            {


                "agent":

                    "GovernanceAgent",


                "trust_score":

                    trust_score,


                "risk_score":

                    risk_percent,


                "decision":

                    decision,


                "runtime_ms":

                    latency_ms


            }

        )









        # =====================================================
        # 10. POSTGRES EXECUTION LEDGER
        # =====================================================


        execution = Execution(


            task=task,


            agent="GovernanceAgent",


            trust_score=trust_score,


            risk_score=risk_percent,


            conflict_score=conflict_score,


            decision=decision,


            result=result,


            latency_ms=latency_ms,


            quality_score=quality_score,


            prompt_tokens=prompt_tokens,


            completion_tokens=completion_tokens


        )




        try:


            db.add(

                execution

            )


            db.commit()



            db.refresh(

                execution

            )


        except Exception as e:


            db.rollback()


            raise e






        return execution