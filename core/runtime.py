from engines.trust_engine import TrustEngine
from engines.risk_engine import RiskEngine
from engines.policy_engine import PolicyEngine


class TrustOSRuntime:

    def __init__(self):
        self.trust_engine = TrustEngine()
        self.risk_engine = RiskEngine()
        self.policy_engine = PolicyEngine()

    def execute(self, task: str):

        trust_score = self.trust_engine.evaluate(task)

        # ✅ analyze (မှန်)
        risk_score = self.risk_engine.analyze(task)

        decision = self.policy_engine.check(
            trust_score,
            risk_score
        )

        return {
            "agent": "RiskAgent",
            "trust_score": trust_score,
            "risk_score": risk_score,
            "decision": decision,
            "result": "Execution completed successfully"
        }