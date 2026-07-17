import time

from engines.governance_engine import GovernanceEngine
from engines.router_engine import RouterEngine
from engines.execution_engine import ExecutionEngine
from engines.telemetry_engine import TelemetryEngine
from engines.audit_engine import AuditEngine


class TrustOSRuntime:
    """
    TrustOSAI Runtime Kernel

    Execution pipeline:

    Request
       |
       v
    Governance Engine
       |
       +---- BLOCK
       |
       +---- ALLOW
                |
                v
          Router Engine
                |
                v
          Execution Engine
                |
                v
          Telemetry
                |
                v
          Audit Ledger
    """

    def __init__(self):

        self.governance_engine = GovernanceEngine()

        self.router_engine = RouterEngine()

        self.execution_engine = ExecutionEngine()

        self.telemetry_engine = TelemetryEngine()

        self.audit_engine = AuditEngine()



    def execute(
        self,
        task: str,
        db=None
    ):

        start = time.perf_counter()


        request_data = {
            "task": task
        }



        # ==================================================
        # 1. Governance Verification Layer
        # ==================================================

        decision, metadata = (
            self.governance_engine.evaluate_request(
                request_data,
                db
            )
        )


        trust_score = (
            metadata
            .get(
                "trust_context",
                {}
            )
            .get(
                "aggregated_trust",
                0
            )
        )


        risk_score = metadata.get(
            "risk_score",
            0
        )



        # ==================================================
        # 2. Governance BLOCK Decision
        # ==================================================

        if decision == "BLOCK":

            result = {

                "agent": "GovernanceAgent",

                "decision": "BLOCK",

                "trust_score": trust_score,

                "risk_score": risk_score,

                "result": "Execution blocked",

                "reason": metadata.get(
                    "reason",
                    "Policy violation"
                )

            }



        # ==================================================
        # 3. Execution ALLOW Decision
        # ==================================================

        else:

            routed_model = (
                self.router_engine.route(
                    task
                )
            )


            execution_result = (
                self.execution_engine.execute(
                    routed_model,
                    task
                )
            )


            result = {

                "agent": routed_model,

                "decision": "ALLOW",

                "trust_score": trust_score,

                "risk_score": risk_score,

                "result": execution_result

            }



        # ==================================================
        # 4. Runtime Measurement
        # ==================================================

        runtime_ms = (
            time.perf_counter()
            -
            start
        ) * 1000


        result["runtime_ms"] = round(
            runtime_ms,
            3
        )



        # ==================================================
        # 5. Telemetry Collection
        # ==================================================

        self.telemetry_engine.collect(
            task,
            result
        )



        # ==================================================
        # 6. Audit Recording
        # ==================================================

        self.audit_engine.record(

            task=task,

            trust=result.get(
                "trust_score",
                0
            ),

            risk=result.get(
                "risk_score",
                0
            ),

            governance=result.get(
                "decision",
                "UNKNOWN"
            ),

            result=result.get(
                "result",
                ""
            )
        )



        return result