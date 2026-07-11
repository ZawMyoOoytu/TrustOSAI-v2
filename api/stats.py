from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Execution



router = APIRouter(
    prefix="/stats",
    tags=["Statistics"]
)



@router.get("/")
def get_stats(
    db:Session = Depends(get_db)
):

    total = (
        db.query(Execution)
        .count()
    )


    allowed = (
        db.query(Execution)
        .filter(
            Execution.decision=="ALLOW"
        )
        .count()
    )


    blocked = (
        db.query(Execution)
        .filter(
            Execution.decision=="BLOCK"
        )
        .count()
    )


    return {

        "total_executions": total,

        "allowed": allowed,

        "blocked": blocked,

        "success_rate":
            round(
                (allowed / total * 100)
                if total > 0 else 0,
                2
            )

    }