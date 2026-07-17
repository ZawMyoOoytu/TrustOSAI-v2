from sqlalchemy.orm import Session
from typing import Dict, Any, Tuple
import time

# ရှေ့က Engine များ၏ Advanced Functions များကို ခေါ်ယူစစ်ဆေးရန်
from engines.trust_engine import TrustEngine
from engines.risk_engine import RiskEngine
from engines.policy_engine import PolicyEngine
from engines.conflict_engine import ConflictEngine

class GovernanceEngine:
    def __init__(self):
        # Base Engines Initialization
        self.trust_engine = TrustEngine()
        self.risk_engine = RiskEngine()
        self.policy_engine = PolicyEngine()
        self.conflict_engine = ConflictEngine()

        # Operational Bounds (စာတမ်းပါ တရားဝင်လုံခြုံရေး Threshold သတ်မှတ်ချက်များ)
        self.min_acceptable_trust = 65.0   # စနစ်လက်ခံနိုင်သော အနိမ့်ဆုံး Trust Score ($\tau$)
        self.max_allowable_risk = 0.70      # စနစ်ခွင့်ပြုနိုင်သော အမြင့်ဆုံး Risk Score

    def evaluate(self, trust_score: float, risk_score: float, policy: str, conflict: bool, context: Any = None) -> Dict[str, Any]:
        """
        Legacy Interface for the standalone legacy RuntimeOrchestrator pipeline.
        Converts parameters to standard dictionary verdict format.
        """
        # Linear Check to preserve backward compatibility
        if trust_score < self.min_acceptable_trust or risk_score > self.max_allowable_risk or policy == "FAILED" or conflict:
            return {"status": "BLOCK", "reason": "Legacy Guardrail Threshold Breached"}
        return {"status": "ALLOW", "reason": "Passed Legacy Thresholds"}

    def evaluate_request(self, request_data: Dict[str, Any], db: Session) -> Tuple[str, Dict[str, Any]]:
        """
        Academic-Grade Holistic Decision Manager.
        Executes all sub-engines sequentially and applies the Comprehensive Verification Matrix.
        Returns: (Decision ["ALLOW" / "BLOCK"], Telemetry/Metadata Matrix)
        """
        start_time = time.time()
        
        # Step 1: Trust Engine Multi-Criteria Assessment
        trust_context = self.trust_engine.evaluate_trust_bounds(request_data, db)
        aggregated_trust = trust_context.get("aggregated_trust", 0.0)

        # Step 2: Risk Engine Signature & PII Scan
        _, normalized_risk, risk_metadata = self.risk_engine.analyze_intent(request_data)

        # Step 3: Policy Engine Static & RBAC Check
        policy_passed, policy_metadata = self.policy_engine.check_constraints(request_data)

        # Step 4: Conflict Engine Concurrency Check
        has_conflict, conflict_metadata = self.conflict_engine.check_concurrency(request_data, db)

        # --------------------------------------------------
        # CRITICAL HOVERING DECISION MATRIX (စာတမ်းပါ သတ်မှတ်ချက် ညီမျှခြင်းများ)
        # --------------------------------------------------
        decision = "ALLOW"
        reject_reason = None
        specific_details = {}

        # Condition A: Static Policy သို့မဟုတ် RBAC ကျိုးဖောက်မှု ရှိမရှိ စစ်ဆေးခြင်း
        if not policy_passed:
            decision = "BLOCK"
            reject_reason = "Static Policy Constraints or Privilege Validation Failed"
            specific_details = policy_metadata.get("violations")

        # Condition B: Operational Risk အလွန်မြင့်မားနေခြင်း (Critical Threat Attack)
        elif normalized_risk > self.max_allowable_risk:
            decision = "BLOCK"
            reject_reason = f"Security Threat Escalation: Risk Score ({normalized_risk}) exceeds maximum threshold ({self.max_allowable_risk})"
            specific_details = risk_metadata.get("threats_identified")

        # Condition C: System Core Trust ကျဆင်းနေခြင်း (Anomalous System State)
        elif aggregated_trust < self.min_acceptable_trust:
            decision = "BLOCK"
            reject_reason = f"System Degradation: Aggregated Trust Score ({aggregated_trust:.2f}) dropped below Safety Threshold ({self.min_acceptable_trust})"
            specific_details = {"system_viability": trust_context.get("is_system_viable")}

        # Condition D: Operational Race Condition / State Drift ဖြစ်ပေါ်နေခြင်း
        elif has_conflict:
            decision = "BLOCK"
            reject_reason = "Operational Concurrency Block: Active Race Condition Detected"
            specific_details = conflict_metadata.get("reason")

        overhead_ms = (time.time() - start_time) * 1000

        # Orchestrator နှင့် API Layer သို့ ပြန်လည်ပေးပို့မည့် Metadata Pack
        metadata = {
            "overhead_ms": overhead_ms,
            "risk_score": normalized_risk,
            "trust_context": trust_context,
            "reason": reject_reason,
            "details": specific_details,
            "sub_engines_telemetry": {
                "risk_metadata": risk_metadata,
                "policy_metadata": policy_metadata,
                "conflict_metadata": conflict_metadata
            }
        }

        return decision, metadata