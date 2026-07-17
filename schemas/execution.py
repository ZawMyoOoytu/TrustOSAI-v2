from datetime import datetime

from pydantic import BaseModel



# ===============================
# Request
# ===============================

class ExecuteRequest(BaseModel):

    task: str



# ===============================
# Governance Response
# ===============================

class GovernanceSchema(BaseModel):

    trust_score: float

    risk_score: float

    conflict_score: float

    decision: str



# ===============================
# Runtime Telemetry
# ===============================

class TelemetrySchema(BaseModel):

    latency_ms: float

    quality_score: float



# ===============================
# Usage / Cost
# ===============================

class UsageSchema(BaseModel):

    prompt_tokens: int

    completion_tokens: int



# ===============================
# Execution Response
# ===============================

class ExecutionResponse(BaseModel):

    execution_id: int

    task: str

    agent: str

    governance: GovernanceSchema

    runtime: TelemetrySchema

    usage: UsageSchema

    result: str

    created_at: datetime


    class Config:

        from_attributes = True