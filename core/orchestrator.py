import time
from sqlalchemy.orm import Session
from typing import Dict, Any

# Engines Imports (ဆရာ့ ဖိုင်တည်ဆောက်ပုံအတိုင်း အပြည့်အစုံ ချိတ်ဆက်ထားပါသည်)
from engines.trust_engine import TrustEngine
from engines.risk_engine import RiskEngine
from engines.policy_engine import PolicyEngine
from engines.memory_engine import MemoryEngine
from engines.conflict_engine import ConflictEngine
from engines.governance_engine import GovernanceEngine
from engines.router_engine import RouterEngine
from engines.execution_engine import ExecutionEngine
from engines.telemetry_engine import TelemetryEngine
from engines.audit_engine import AuditEngine
from engines.cost_engine import CostEngine

class RuntimeOrchestrator:

    def __init__(self):
        # Core Governance Controllers
        self.trust_engine = TrustEngine()
        self.risk_engine = RiskEngine()
        self.policy_engine = PolicyEngine()
        self.memory_engine = MemoryEngine()
        self.conflict_engine = ConflictEngine()
        self.governance_engine = GovernanceEngine()
        
        # Routing & Execution Core
        self.router_engine = RouterEngine()
        self.execution_engine = ExecutionEngine()
        
        # Telemetry, Cost & Logging Framework
        self.audit_engine = AuditEngine()
        self.telemetry_engine = TelemetryEngine()
        self.cost_engine = CostEngine()

    def execute(self, task: str, db: Session) -> Dict[str, Any]:
        """
        Executes the entire TrustOSAI secure pipeline matching the paper workflow.
        Includes Early Termination Guards and Asynchronous Feedback Loops.
        """
        pipeline_start_time = time.time()
        
        # --------------------------------------------------
        # PHASE 1: GOVERNANCE CONTROL CORE & SUB-ENGINES
        # --------------------------------------------------
        # Step 1: Evaluate Trust Vectors (MCDM Boundaries)
        trust_score = self.trust_engine.evaluate(task, db)

        # Step 2: Intent Risk & PII Scans
        risk_score = self.risk_engine.analyze(task)

        # Step 3: Check Static/Attribute Policies
        policy_result = self.policy_engine.check(trust_score, risk_score)

        # Step 4: Semantic Context Retrieval (L2 Memory Cache)
        semantic_context = self.memory_engine.retrieve_context(task, db)

        # Step 5: State Concurrency & Cross-Agent Conflict Detection
        conflict = self.conflict_engine.detect(task, policy_result, db)

        # Step 6: Decision Manager Consolidation
        # Combines all vectors and determines "ALLOW" or "BLOCK"
        governance = self.governance_engine.evaluate(
            trust_score=trust_score,
            risk_score=risk_score,
            policy=policy_result,
            conflict=conflict,
            context=semantic_context
        )

        # --------------------------------------------------
        # PHASE 2: DECISION SPLITTING & EARLY TERMINATION
        # --------------------------------------------------
        governance_status = governance.get("status", "BLOCK")
        governance_overhead = (time.time() - pipeline_start_time) * 1000

        if governance_status == "BLOCK":
            # Early Termination Route: Audit Failure and Return Immediately
            self.audit_engine.record(
                db=db, task=task, trust_score=trust_score, risk_score=risk_score,
                governance=governance, execution_result="TERMINATED BY GOVERNANCE", cost=0.0
            )
            return {
                "decision": "BLOCK",
                "reason": governance.get("reason", "Security Policy Anomaly"),
                "governance_overhead_ms": governance_overhead
            }

        # --------------------------------------------------
        # PHASE 3: OPTIMAL ROUTING & GRAPH COMPILATION
        # --------------------------------------------------
        # Step 7: Select Target Optimal Model/Agent (m*)
        route = self.router_engine.route(governance)

        # --------------------------------------------------
        # PHASE 4: RUNTIME EXECUTOR
        # --------------------------------------------------
        # Step 8: Execution Graph Handling & Response Generation
        execution_start_time = time.time()
        execution_result = self.execution_engine.execute(route, task)
        execution_latency = (time.time() - execution_start_time) * 1000

        # --------------------------------------------------
        # PHASE 5: POST-EXECUTION TELEMETRY & FEEDBACK LOOP
        # --------------------------------------------------
        # Step 9: Real-time API Cost & Token tracking
        cost = self.cost_engine.calculate(route, task, execution_result)

        # Step 10: Persistent Audit Logging (L3 Memory Vault)
        self.audit_engine.record(
            db=db, task=task, trust_score=trust_score, risk_score=risk_score,
            governance=governance, execution_result=execution_result, cost=cost
        )

        # Step 11: Collect Quality Index (Q_t) and Latency Metrics
        telemetry = self.telemetry_engine.collect(task, execution_result, execution_latency)

        # Step 12: Closed-Loop Memory Update & Trust Score Mutation Trigger
        # Propagates Q_t back to PostgreSQL to alter future Trust Engine calculations
        self.memory_engine.update_memory(
            db=db, task=task, response=execution_result, quality_score=telemetry.get("quality_score")
        )

        total_pipeline_latency = (time.time() - pipeline_start_time) * 1000

        return {
            "decision": "ALLOW",
            "task": task,
            "trust_score": trust_score,
            "risk_score": risk_score,
            "policy": policy_result,
            "conflict": conflict,
            "governance": governance,
            "route": route,
            "result": execution_result,
            "telemetry": {
                "governance_overhead_ms": governance_overhead,
                "execution_latency_ms": execution_latency,
                "total_latency_ms": total_pipeline_latency,
                "cost_incurred": cost,
                "quality_index": telemetry.get("quality_score")
            }
        }