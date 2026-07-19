from fastapi import FastAPI

from database.connection import Base, engine

# Load all models
import database.models


from api.routes import router



# ==================================================
# Database Initialization
# ==================================================

Base.metadata.create_all(
    bind=engine
)



# ==================================================
# FastAPI Application
# ==================================================

app = FastAPI(

    title="TrustOSAI PostgreSQL Runtime",

    version="2.0.0",

    description="""
TrustOSAI Adaptive AI Governance Runtime.

Features:

- Trust Evaluation
- Risk Detection
- Policy Enforcement
- Conflict Analysis
- Governance Decision
- Execution Telemetry
- Cost Attribution
- Audit Logging
"""

)



# ==================================================
# Register API
# ==================================================

app.include_router(
    router
)



# ==================================================
# Root
# ==================================================

@app.get("/")
def root():

    return {

        "system":
            "TrustOSAI",

        "architecture":
            "Trust-aware AI Execution Control Plane",

        "runtime":
            "Production Governance Runtime",

        "database":
            "PostgreSQL",

        "version":
            "2.0.0",

        "status":
            "online"

    }