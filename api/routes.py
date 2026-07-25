from fastapi import APIRouter



# =====================================================
# TRUSTOSAI API REGISTRY
# =====================================================


from api.agents import router as agents_router


from api.execution import router as execution_router


from api.executions import router as executions_router


from api.replay import router as replay_router



from api.policy import router as policy_router


from api.trust import router as trust_router


from api.reasoning import router as reasoning_router



from api.stats import router as stats_router


from api.health import router as health_router





# =====================================================
# ROOT ROUTER
# =====================================================


router = APIRouter(
    prefix="/api"
)





# =====================================================
# AGENT MANAGEMENT
# =====================================================


router.include_router(
    agents_router
)





# =====================================================
# EXECUTION
# =====================================================


router.include_router(
    execution_router
)


router.include_router(
    executions_router
)





# =====================================================
# REPLAY
# =====================================================


router.include_router(
    replay_router
)





# =====================================================
# GOVERNANCE
# =====================================================


router.include_router(
    policy_router
)


router.include_router(
    trust_router
)


router.include_router(
    reasoning_router
)





# =====================================================
# ANALYTICS
# =====================================================


router.include_router(
    stats_router
)





# =====================================================
# HEALTH
# =====================================================


router.include_router(
    health_router
)