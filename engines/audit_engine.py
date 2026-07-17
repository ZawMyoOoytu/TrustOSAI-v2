from datetime import datetime


class AuditEngine:
    """
    TrustOSAI Audit Engine

    Responsible for:
    - Runtime execution audit
    - Governance decision tracking
    - Trust/Risk traceability
    - Compliance evidence generation
    """


    def __init__(self):

        self.audit_logs = []



    # =====================================================
    # Record Execution Event
    # =====================================================

    def record(
        self,
        task,
        trust,
        risk,
        governance,
        result
    ):

        audit_event = {

            "timestamp":
                datetime.utcnow(),

            "task":
                task,

            "trust_score":
                trust,

            "risk_score":
                risk,

            "governance":
                governance,

            "result":
                result

        }


        self.audit_logs.append(
            audit_event
        )


        return audit_event



    # =====================================================
    # Retrieve Audit History
    # =====================================================

    def get_logs(
        self,
        limit=50
    ):

        return (
            self.audit_logs[-limit:]
        )



    # =====================================================
    # Clear Logs
    # =====================================================

    def clear(self):

        self.audit_logs = []