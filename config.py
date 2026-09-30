import os


# =========================
# TrustOSAI Application
# =========================

APP_NAME = "TrustOSAI"

APP_VERSION = "2.1.0"


ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development"
)



# =========================
# Database Configuration
# =========================

DATABASE_URL = os.getenv(

    "DATABASE_URL",

    "postgresql://trustos:trustos123@localhost:5432/trustos_db"

)



# =========================
# Governance Configuration
# =========================

# Minimum trust score required

TRUST_THRESHOLD = float(

    os.getenv(
        "TRUST_THRESHOLD",
        "0.75"
    )

)



# Maximum allowed risk score

RISK_THRESHOLD = float(

    os.getenv(
        "RISK_THRESHOLD",
        "0.5"
    )

)



# Minimum policy compliance score

POLICY_THRESHOLD = float(

    os.getenv(
        "POLICY_THRESHOLD",
        "0.8"
    )

)