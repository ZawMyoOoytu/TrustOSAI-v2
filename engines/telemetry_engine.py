from datetime import datetime
from sqlalchemy.orm import Session


class TelemetryEngine:

    def __init__(self):
        self.status = "READY"


    # =====================================================
    # Main telemetry collector
    # =====================================================

    def collect(
        self,
        task: str,
        result: dict
    ) -> dict:

        telemetry_data = {

            "task_preview":
                task[:50]
                if task
                else "",


            "assigned_agent":
                result.get(
                    "agent",
                    "GovernanceAgent"
                ),


            "evaluated_trust":
                float(
                    result.get(
                        "trust_score",
                        0.0
                    )
                ),


            "evaluated_risk":
                float(
                    result.get(
                        "risk_score",
                        0.0
                    )
                ),


            "final_decision":
                result.get(
                    "decision",
                    "BLOCK"
                ),


            "latency_overhead_ms":
                result.get(
                    "runtime_ms",
                    0
                ),


            "status":
                (
                    "SUCCESS"
                    if result.get("decision")
                    in [
                        "ALLOW",
                        "APPROVE",
                        "APPROVED"
                    ]
                    else
                    "MITIGATED"
                ),


            "timestamp":
                datetime.utcnow()

        }


        return telemetry_data



    # =====================================================
    # Runtime measurement interface
    # Used by ExecutionService
    # =====================================================

    def measure(
        self,
        task: str,
        latency_ms: int,
        decision: str,
        db: Session = None
    ) -> dict:


        telemetry = {


            "task_preview":
                task[:50],


            "latency_ms":
                latency_ms,


            "decision":
                decision,


            "status":
                (
                    "SUCCESS"
                    if decision
                    in [
                        "APPROVE",
                        "APPROVED",
                        "ALLOW"
                    ]
                    else
                    "BLOCKED"
                ),


            "created_at":
                datetime.utcnow()

        }



        # Future:
        # if db:
        #     save telemetry table


        return telemetry