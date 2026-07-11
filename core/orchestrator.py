from engines.trust_engine import TrustEngine
from engines.risk_engine import RiskEngine
from engines.policy_engine import PolicyEngine
from engines.conflict_engine import ConflictEngine
from engines.governance_engine import GovernanceEngine
from engines.router_engine import RouterEngine
from engines.execution_engine import ExecutionEngine
from engines.audit_engine import AuditEngine
from engines.telemetry_engine import TelemetryEngine


class RuntimeOrchestrator:

    def __init__(self):

        self.trust_engine = TrustEngine()
        self.risk_engine = RiskEngine()
        self.policy_engine = PolicyEngine()

        self.conflict_engine = ConflictEngine()
        self.governance_engine = GovernanceEngine()

        self.router_engine = RouterEngine()
        self.execution_engine = ExecutionEngine()

        self.audit_engine = AuditEngine()
        self.telemetry_engine = TelemetryEngine()

    def execute(self, task: str):

        # Step 1
        trust_score = self.trust_engine.evaluate(task)

        # Step 2
        risk_score = self.risk_engine.analyze(task)

        # Step 3
        policy_result = self.policy_engine.check(
            trust_score,
            risk_score
        )

        # Step 4
        conflict = self.conflict_engine.detect(
            task,
            policy_result
        )

        # Step 5
        governance = self.governance_engine.evaluate(
            trust_score,
            risk_score,
            policy_result,
            conflict
        )

        # Step 6
        route = self.router_engine.route(
            governance
        )

        # Step 7
        execution_result = self.execution_engine.execute(
            route,
            task
        )

        # Step 8
        self.audit_engine.record(
            task,
            trust_score,
            risk_score,
            governance,
            execution_result
        )

        # Step 9
        self.telemetry_engine.collect(
            task,
            execution_result
        )

        return {
            "task": task,
            "trust_score": trust_score,
            "risk_score": risk_score,
            "policy": policy_result,
            "conflict": conflict,
            "governance": governance,
            "route": route,
            "result": execution_result
        }