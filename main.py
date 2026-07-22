from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware



from database.connection import (
    Base,
    engine
)



# ==================================================
# Load Database Models
# ==================================================

import database.models





# ==================================================
# API ROUTER
# api/routes.py
# ==================================================

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



"""


)









# ==================================================
# CORS Configuration
# Frontend: Vite React
# ==================================================


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









# ==================================================
# Register All API Routes
#
# api/routes.py handles:
#
# /api/agents
# /api/executions
# /api/policy
# /api/trust
# ...
#
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

            "Model Router",

            "Execution Replay",

            "Audit Telemetry"

        ],



        "status":

            "online"


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

            "TrustOSAI Runtime",



        "version":

            "2.0.0"


    }