from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from sqlalchemy import func

from database.connection import get_db

from database.models import Execution



router = APIRouter(
    prefix="/stats",
    tags=[
        "Statistics"
    ]
)





# =====================================================
# TRUSTOSAI DASHBOARD STATISTICS
# =====================================================


@router.get("/")
def get_stats(

    db: Session = Depends(get_db)

):


    # =============================================
    # TOTAL EXECUTIONS
    # =============================================


    total = (
        db.query(
            Execution
        )
        .count()
    )





    # =============================================
    # ALLOWED
    #
    # Successful Governance Decisions
    #
    # =============================================


    allowed = (
        db.query(
            Execution
        )
        .filter(
            Execution.decision.in_(
                [
                    "ALLOW",
                    "ALLOW_WITH_MONITORING",
                    "APPROVED",
                    "ALLOWED"
                ]
            )
        )
        .count()
    )





    # =============================================
    # MONITORING
    # =============================================


    monitoring = (
        db.query(
            Execution
        )
        .filter(
            Execution.decision==
            "ALLOW_WITH_MONITORING"
        )
        .count()
    )





    # =============================================
    # BLOCKED
    # =============================================


    blocked = (
        db.query(
            Execution
        )
        .filter(
            Execution.decision.in_(
                [
                    "BLOCK",
                    "BLOCKED"
                ]
            )
        )
        .count()
    )





    # =============================================
    # HUMAN REVIEW
    # =============================================


    review = (
        db.query(
            Execution
        )
        .filter(
            Execution.decision==
            "REVIEW"
        )
        .count()
    )





    # =============================================
    # TRUST SCORE
    # =============================================


    avg_trust = (
        db.query(
            func.avg(
                Execution.trust_score
            )
        )
        .scalar()
        or 0
    )





    # =============================================
    # RUNTIME
    # =============================================


    avg_runtime = (
        db.query(
            func.avg(
                Execution.runtime_ms
            )
        )
        .scalar()
        or 0
    )





    # =============================================
    # LATENCY
    # =============================================


    avg_latency = (
        db.query(
            func.avg(
                Execution.latency_ms
            )
        )
        .scalar()
        or 0
    )





    # =============================================
    # COST
    # =============================================


    total_cost = (
        db.query(
            func.sum(
                Execution.cost_usd
            )
        )
        .scalar()
        or 0
    )





    # =============================================
    # SUCCESS RATE
    #
    # ALLOW
    # ALLOW_WITH_MONITORING
    #
    # =============================================


    success_rate = 0


    if total > 0:

        success_rate = round(
            (
                allowed /
                total
            )
            *
            100,

            2
        )





    return {


        "total_executions":
            total,



        "allowed":
            allowed,



        "monitoring":
            monitoring,



        "blocked":
            blocked,



        "review":
            review,



        "average_trust":
            round(
                float(avg_trust),
                2
            ),



        "average_trust_score":
            round(
                float(avg_trust),
                2
            ),



        "average_latency_ms":
            round(
                float(avg_latency),
                2
            ),



        "runtime_ms":
            round(
                float(avg_runtime),
                2
            ),



        "total_cost_usd":
            round(
                float(total_cost),
                4
            ),



        "success_rate":
            success_rate

    }