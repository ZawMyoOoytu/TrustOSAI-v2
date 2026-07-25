from contextlib import asynccontextmanager


from fastapi import FastAPI


from fastapi.middleware.cors import CORSMiddleware



from sqlalchemy import text


from database.connection import (
    Base,
    engine,
    SessionLocal
)



# =====================================================
# LOAD DATABASE MODELS
# =====================================================

import database.models





# =====================================================
# API ROUTER
# =====================================================


from api.routes import router





# =====================================================
# APPLICATION LIFESPAN
# =====================================================


@asynccontextmanager
async def lifespan(app: FastAPI):


    print(
        "⚡ Starting TrustOSAI Runtime..."
    )


    # ---------------------------------------------
    # Create Database Tables
    # ---------------------------------------------


    Base.metadata.create_all(
        bind=engine
    )



    print(
        "✅ Database initialized"
    )


    yield



    print(
        "🛑 TrustOSAI Runtime shutdown"
    )







# =====================================================
# FASTAPI APPLICATION
# =====================================================


app = FastAPI(


    title="TrustOSAI PostgreSQL Runtime",


    version="2.0.0",


    description="""


TrustOSAI Adaptive AI Governance Runtime.



Core Capabilities:


- Agent Registry

- Trust Evaluation

- Risk Detection

- Policy Enforcement

- Conflict Analysis

- Governance Decision

- Model Routing

- Execution Telemetry

- Cost Attribution

- Audit Logging

- Execution Replay

- AI Runtime Control Plane



""",


    lifespan=lifespan

)







# =====================================================
# CORS
# =====================================================


app.add_middleware(


    CORSMiddleware,


    allow_origins=[


        "http://localhost:5173",


        "http://localhost:5174",


        "http://127.0.0.1:5173",


        "http://127.0.0.1:5174"


    ],



    allow_credentials=True,



    allow_methods=[
        "*"
    ],



    allow_headers=[
        "*"
    ]

)








# =====================================================
# REGISTER ROUTERS
# =====================================================


app.include_router(

    router

)







# =====================================================
# ROOT
# =====================================================


@app.get("/")


def root():


    return {


        "system":
            "TrustOSAI",



        "architecture":
            "Trust-aware AI Execution Control Plane",



        "runtime":
            "Adaptive AI Governance Runtime",



        "database":
            "PostgreSQL",



        "version":
            "2.0.0",



        "features":[


            "Agent Registry",


            "Policy Engine",


            "Trust Engine",


            "Risk Engine",


            "Conflict Engine",


            "Model Router",


            "Execution Replay",


            "Memory Engine",


            "Cost Attribution",


            "Audit Telemetry"


        ],



        "status":
            "online"

    }








# =====================================================
# HEALTH CHECK
# =====================================================


@app.get("/health")


def health():


    database_status = "offline"



    try:


        db = SessionLocal()


        db.execute(
            text(
                "SELECT 1"
            )
        )


        database_status = "online"



    except Exception:


        database_status = "offline"



    finally:


        try:

            db.close()

        except:

            pass





    return {


        "status":
            "healthy",



        "service":
            "TrustOSAI Runtime",



        "version":
            "2.0.0",



        "database":
            database_status

    }