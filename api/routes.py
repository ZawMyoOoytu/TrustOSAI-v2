from fastapi import APIRouter


from api.execution import router as execution_router
from api.executions import router as executions_router
from api.health import router as health_router
from api.policy import router as policy_router
from api.stats import router as stats_router



router = APIRouter()



router.include_router(
    execution_router
)


router.include_router(
    executions_router
)


router.include_router(
    health_router
)


router.include_router(
    policy_router
)


router.include_router(
    stats_router
)