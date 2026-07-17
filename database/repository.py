from sqlalchemy.orm import Session
from sqlalchemy import func

from database.models import Execution


class MetricsRepository:
    """
    TrustOSAI Metrics Repository

    Provides historical execution intelligence
    for Trust Engine, Governance Engine,
    and Runtime Analytics.

    Responsibilities:
    - Execution history retrieval
    - Trust score analysis
    - Risk measurement
    - Policy compliance evaluation
    - Runtime efficiency calculation
    """



    def __init__(self, db: Session):

        self.db = db



    # =====================================================
    # Recent Execution History
    # =====================================================

    def get_recent_execution_logs(
        self,
        limit: int = 20
    ):

        return (
            self.db
            .query(Execution)
            .order_by(
                Execution.created_at.desc()
            )
            .limit(limit)
            .all()
        )



    # =====================================================
    # Policy Compliance Rate
    #
    # Compliance =
    # ALLOW executions / Total executions
    #
    # =====================================================

    def get_policy_compliance_rate(self):

        total = (
            self.db
            .query(Execution)
            .count()
        )


        if total == 0:
            return 1.0



        allowed = (
            self.db
            .query(Execution)
            .filter(
                Execution.decision == "ALLOW"
            )
            .count()
        )


        return round(
            allowed / total,
            4
        )



    # =====================================================
    # Average Trust Score
    # =====================================================

    def get_average_trust_score(self):

        result = (
            self.db
            .query(
                func.avg(
                    Execution.trust_score
                )
            )
            .scalar()
        )


        if result is None:
            return 0.0


        return round(
            float(result),
            4
        )



    # =====================================================
    # Average Risk Score
    # =====================================================

    def get_average_risk_score(self):

        result = (
            self.db
            .query(
                func.avg(
                    Execution.risk_score
                )
            )
            .scalar()
        )


        if result is None:
            return 0.0


        return round(
            float(result),
            4
        )



    # =====================================================
    # Total Execution Count
    # =====================================================

    def get_execution_count(self):

        return (
            self.db
            .query(Execution)
            .count()
        )



    # =====================================================
    # Blocked Execution Count
    # =====================================================

    def get_blocked_execution_count(self):

        return (
            self.db
            .query(Execution)
            .filter(
                Execution.decision == "BLOCK"
            )
            .count()
        )



    # =====================================================
    # Average Runtime Latency
    # =====================================================

    def get_average_latency(self):

        result = (
            self.db
            .query(
                func.avg(
                    Execution.latency_ms
                )
            )
            .scalar()
        )


        if result is None:
            return 0.0


        return round(
            float(result),
            4
        )



    # =====================================================
    # Average Quality Score Q_t
    #
    # Used by Trust Evolution Equation
    #
    # =====================================================

    def get_average_quality_score(self):

        result = (
            self.db
            .query(
                func.avg(
                    Execution.quality_score
                )
            )
            .scalar()
        )


        if result is None:
            return 0.85


        return round(
            float(result),
            4
        )



    # =====================================================
    # Cost Efficiency Index
    #
    # Efficiency =
    # 1 / (1 + latency_seconds)
    #
    # Range: 0 - 1
    #
    # =====================================================

    def get_cost_efficiency_index(self):

        avg_latency = (
            self.get_average_latency()
        )


        if avg_latency <= 0:

            return 1.0



        latency_seconds = (
            avg_latency / 1000.0
        )


        efficiency = (
            1 /
            (
                1 +
                latency_seconds
            )
        )


        return round(
            min(
                max(
                    efficiency,
                    0.0
                ),
                1.0
            ),
            4
        )



    # =====================================================
    # Successful Execution Count
    # =====================================================

    def get_success_count(self):

        return (
            self.db
            .query(Execution)
            .filter(
                Execution.decision == "ALLOW"
            )
            .count()
        )



    # =====================================================
    # Failure Rate
    #
    # BLOCK / TOTAL
    #
    # =====================================================

    def get_failure_rate(self):

        total = (
            self.get_execution_count()
        )


        if total == 0:
            return 0.0


        blocked = (
            self.get_blocked_execution_count()
        )


        return round(
            blocked / total,
            4
        )
            # =====================================================
    # Cost Efficiency Index
    # =====================================================

    def get_cost_efficiency_index(self):

        executions = (

            self.db
            .query(Execution)
            .all()

        )


        if not executions:

            return 1.0



        values = []


        for item in executions:


            latency = getattr(
                item,
                "latency_ms",
                0
            )


            if latency == 0:

                values.append(1.0)


            else:

                efficiency = (

                    1 /

                    (
                        1
                        +
                        latency / 1000
                    )

                )


                values.append(
                    efficiency
                )



        return round(

            sum(values)
            /
            len(values),

            4

        )