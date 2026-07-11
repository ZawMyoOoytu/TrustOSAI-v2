from fastapi import APIRouter

from api.execution import router as execution_router
from api.policy import router as policy_router
from api.health import router as health_router


router = APIRouter()


router.include_router(
    execution_router,
    prefix="/api"
)


router.include_router(
    policy_router,
    prefix="/api"
)


router.include_router(
    health_router,
    prefix="/api"
)