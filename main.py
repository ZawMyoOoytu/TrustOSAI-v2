from fastapi import FastAPI

from database.session import Base, engine

from api.routes import router


# ==================================================
# Import Models
# Required for SQLAlchemy registration
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

    description=
    "Trust-aware AI Governance Runtime with Execution Control"

)



# ==================================================
# API Routes
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



# ==================================================
# Health Check
# ==================================================

@app.get("/health")
def health():

    return {

        "status":
        "healthy",

        "service":
        "TrustOSAI API",

        "database":
        "connected"

    }