from fastapi import APIRouter



# =====================================================
# TRUSTOSAI API ROUTER REGISTRY
# =====================================================



# -----------------------------------------------------
# Agent Registry
# -----------------------------------------------------

from api.agents import router as agents_router





# -----------------------------------------------------
# Execution Runtime
# -----------------------------------------------------

from api.execution import router as execution_router

from api.executions import router as executions_router





# -----------------------------------------------------
# Replay Engine
# -----------------------------------------------------

from api.replay import router as replay_router





# -----------------------------------------------------
# Governance Services
# -----------------------------------------------------

from api.policy import router as policy_router

from api.trust import router as trust_router

from api.reasoning import router as reasoning_router





# -----------------------------------------------------
# Observability
# -----------------------------------------------------

from api.stats import router as stats_router





# -----------------------------------------------------
# System
# -----------------------------------------------------

from api.health import router as health_router







# =====================================================
# ROOT API ROUTER
# =====================================================

router = APIRouter()







# =====================================================
# 1. AGENT REGISTRY
#
# Provides:
#
# POST   /api/agents/
# GET    /api/agents/
# GET    /api/agents/{id}
# PATCH  /api/agents/{id}
# PATCH  /api/agents/{id}/disable
# GET    /api/agents/{id}/stats
#
# =====================================================


router.include_router(

    agents_router

)









# =====================================================
# 2. EXECUTION PIPELINE
#
# Provides:
#
# POST /api/execution
# GET  /api/executions
#
# =====================================================


router.include_router(

    execution_router

)



router.include_router(

    executions_router

)









# =====================================================
# 3. EXECUTION REPLAY ENGINE
#
# Provides:
#
# Replay original execution
# Compare executions
#
# =====================================================


router.include_router(

    replay_router

)









# =====================================================
# 4. TRUST GOVERNANCE LAYER
#
# Policy Engine
# Trust Engine
# Reasoning Engine
#
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
# 5. TELEMETRY / ANALYTICS
#
# Statistics
# Metrics
# Dashboard Data
#
# =====================================================


router.include_router(

    stats_router

)









# =====================================================
# 6. HEALTH CHECK
#
# System Monitoring
#
# =====================================================


router.include_router(

    health_router

)