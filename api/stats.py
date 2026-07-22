from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database.connection import get_db
from database.models import Execution


router = APIRouter(
    prefix="/stats",
    tags=["Statistics"]
)



@router.get("/")
def get_stats(
    db: Session = Depends(get_db)
):


    total = (
        db.query(Execution)
        .count()
    )



    allowed = (
        db.query(Execution)
        .filter(
            Execution.decision.in_(
                [
                    "APPROVED",
                    "ALLOW",
                    "ALLOWED"
                ]
            )
        )
        .count()
    )



    blocked = (
        db.query(Execution)
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



    review = (
        db.query(Execution)
        .filter(
            Execution.decision=="REVIEW"
        )
        .count()
    )



    avg_trust = (
        db.query(
            func.avg(
                Execution.trust_score
            )
        )
        .scalar()
    )



    avg_runtime = (
        db.query(
            func.avg(
                Execution.runtime_ms
            )
        )
        .scalar()
    )



    success_rate = 0


    if total > 0:

        success_rate = round(
            (allowed / total) * 100,
            2
        )



    return {


        "total_executions":
            total,


        "allowed":
            allowed,


        "blocked":
            blocked,


        "review":
            review,


        "success_rate":
            success_rate,



        "average_trust_score":
            round(
                float(avg_trust or 0),
                2
            ),



        "runtime_ms":
            round(
                float(avg_runtime or 0),
                2
            )

    }