from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta


from database.models import Execution



class MetricsRepository:
    """
    TrustOSAI Database Intelligence Repository


    Responsibilities:

    - Execution history retrieval
    - Trust feedback calculation
    - Failure analysis
    - Cost efficiency measurement
    - Conflict detection

    """



    def __init__(
        self,
        db: Session
    ):

        self.db = db



    # =====================================================
    # Recent Execution Logs
    # =====================================================

    def get_recent_execution_logs(
        self,
        limit=20
    ):


        return (

            self.db.query(
                Execution
            )

            .order_by(
                desc(
                    Execution.created_at
                )
            )

            .limit(limit)

            .all()

        )




    # =====================================================
    # Failure Rate
    # =====================================================

    def get_failure_rate(self):


        total = (

            self.db.query(
                Execution
            )

            .count()

        )



        if total == 0:

            return 0.0




        failed = (

            self.db.query(
                Execution
            )

            .filter(

                Execution.decision
                ==

                "BLOCK"

            )

            .count()

        )



        return failed / total




    # =====================================================
    # Policy Compliance Rate
    # =====================================================

    def get_policy_compliance_rate(self):


        total = (

            self.db.query(
                Execution
            )

            .count()

        )



        if total == 0:

            return 0.85



        approved = (

            self.db.query(
                Execution
            )

            .filter(

                Execution.decision
                .in_(
                    [
                        "ALLOW",
                        "APPROVED"
                    ]
                )

            )

            .count()

        )



        return approved / total




    # =====================================================
    # Cost Efficiency Index
    # =====================================================

    def get_cost_efficiency_index(self):


        logs = self.get_recent_execution_logs(
            20
        )



        if not logs:

            return 0.85



        scores=[]



        for log in logs:


            latency=getattr(

                log,

                "latency_ms",

                0

            )



            if latency <= 500:


                scores.append(
                    1.0
                )


            elif latency <= 2000:


                scores.append(
                    0.8
                )


            else:


                scores.append(
                    0.5
                )



        return sum(scores)/len(scores)





    # =====================================================
    # Duplicate Task Conflict Detection
    # =====================================================

    def get_duplicate_tasks_within_window(
        self,
        task_snippet:str,
        seconds_window:float
    ):


        threshold = (

            datetime.utcnow()

            -

            timedelta(
                seconds=seconds_window
            )

        )



        return (

            self.db.query(
                Execution
            )

            .filter(

                Execution.task
                .ilike(
                    f"%{task_snippet}%"
                ),

                Execution.created_at
                >=
                threshold

            )

            .all()

        )