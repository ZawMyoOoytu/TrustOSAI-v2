from fastapi import FastAPI

from database.connection import Base, engine

from api.routes import router


# ==================================================
# Import Database Models
# Required for SQLAlchemy table registration
# ==================================================

from database.models import Execution



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

    version="2.0",

    description=(
        "Trust-aware AI Governance Runtime "
        "with Execution Control"
    )

)



# ==================================================
# API Router Registration
# ==================================================

app.include_router(
    router
)



# ==================================================
# Root Endpoint
# ==================================================

@app.get("/")
def root():

    return {

        "system": "TrustOSAI",

        "runtime":
            "Governance Execution Runtime",

        "database":
            "PostgreSQL",

        "version":
            "2.0",

        "status":
            "running"

    }