from fastapi import APIRouter


router = APIRouter(
    prefix="/policy",
    tags=["Policy"]
)


@router.get("/")
def get_policy():

    return {

        "policy_engine": "active",

        "threshold": 0.8,

        "status": "running"

    }