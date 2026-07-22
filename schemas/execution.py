from datetime import datetime

from typing import Optional, Dict, Any, List

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)



# =====================================================
# EXECUTE REQUEST
# =====================================================


class ExecuteRequest(BaseModel):

    task: str = Field(
        ...,
        min_length=2
    )


    agent_id: Optional[int] = None


    agent: Optional[str] = None


    model: Optional[str] = "local"


    provider: Optional[str] = "local"


    api_key: Optional[str] = None


    metadata_json: Optional[
        Dict[str, Any]
    ] = None



    model_config = ConfigDict(
        from_attributes=True
    )







# =====================================================
# TOKEN TELEMETRY
# =====================================================


class TokenTelemetryResponse(BaseModel):


    prompt_tokens: int = 0


    completion_tokens: int = 0


    total_tokens: int = 0


    context_window: int = 0



    model_config = ConfigDict(
        from_attributes=True
    )







# =====================================================
# COST
# =====================================================


class CostResponse(BaseModel):


    input_tokens: int = 0


    output_tokens: int = 0


    total_tokens: int = 0


    input_cost: float = 0.0


    output_cost: float = 0.0


    total_cost: float = 0.0


    currency: str = "USD"



    model_config = ConfigDict(
        from_attributes=True
    )







# =====================================================
# EXECUTION RESPONSE
# =====================================================


class ExecutionResponse(BaseModel):


    execution_id: int


    task: str



    agent: Optional[str] = None


    agent_id: Optional[int] = None



    trust_score: float = 0.0


    risk_score: float = 0.0


    conflict_score: float = 0.0



    decision: str = "REVIEW"



    reasoning: Optional[str] = None




    # FIX:
    # Runtime returns dict/json
    result: Optional[
        Dict[str,Any]
    ] = None




    status: str = "COMPLETED"



    quality_score: float = 0.0



    latency_ms: float = 0.0


    runtime_ms: float = 0.0




    provider: Optional[str] = None


    model: Optional[str] = None




    cost: Optional[
        CostResponse
    ] = None




    token_telemetry: Optional[
        TokenTelemetryResponse
    ] = None




    execution_type: str = "NORMAL"



    parent_execution_id: Optional[int] = None




    metadata_json: Optional[
        Dict[str,Any]
    ] = None




    created_at: Optional[
        datetime
    ] = None




    model_config = ConfigDict(
        from_attributes=True
    )







# =====================================================
# DETAIL RESPONSE
# =====================================================


class ExecutionDetailResponse(
    ExecutionResponse
):


    policy_trace: Optional[
        Dict[str,Any]
    ] = None



    audit_log: Optional[
        Dict[str,Any]
    ] = None



    memory_context: Optional[
        Dict[str,Any]
    ] = None



    execution_graph: Optional[
        Dict[str,Any]
    ] = None







# =====================================================
# LIST RESPONSE
# =====================================================


class ExecutionListResponse(BaseModel):


    items: List[
        ExecutionResponse
    ] = Field(
        default_factory=list
    )



    model_config = ConfigDict(
        from_attributes=True
    )







# =====================================================
# REPLAY REQUEST
# =====================================================


class ReplayRequest(BaseModel):


    execution_type: str = "REPLAY"


    model: Optional[str] = None


    provider: Optional[str] = None



    metadata_json: Optional[
        Dict[str,Any]
    ] = None



    model_config = ConfigDict(
        from_attributes=True
    )







# =====================================================
# REPLAY RESULT
# =====================================================


class ReplayResultResponse(BaseModel):


    execution_id: int


    execution_mode: str = "REPLAY"



    task: Optional[str] = None



    agent: Optional[str] = None



    model: Optional[str] = None


    provider: Optional[str] = None




    decision: str = "REVIEW"



    trust_score: float = 0


    risk_score: float = 0


    conflict_score: float = 0



    quality_score: float = 0



    runtime_ms: float = 0



    latency_ms: float = 0




    result: Optional[
        Dict[str,Any]
    ] = None




    token_telemetry: Optional[
        TokenTelemetryResponse
    ] = None




    parent_execution_id: Optional[int] = None



    execution_type: str = "REPLAY"







# =====================================================
# REPLAY RESPONSE
# =====================================================


class ReplayResponse(BaseModel):


    replay: bool = True



    original_execution_id: int



    replay_execution_id: int



    execution_type: str = "REPLAY"



    parent_execution_id: Optional[int] = None




    replay_result: ReplayResultResponse




    model_config = ConfigDict(
        from_attributes=True
    )







# =====================================================
# STATS
# =====================================================


class ExecutionStatsResponse(BaseModel):


    total_executions: int = 0


    allowed: int = 0


    blocked: int = 0


    review: int = 0



    average_trust: float = 0



    average_latency_ms: float = 0



    total_cost_usd: float = 0



    success_rate: float = 0



    model_config = ConfigDict(
        from_attributes=True
    )







# =====================================================
# EXPORT
# =====================================================


__all__ = [


    "ExecuteRequest",


    "ExecutionResponse",


    "ExecutionDetailResponse",


    "ExecutionListResponse",


    "ExecutionStatsResponse",


    "ReplayRequest",


    "ReplayResponse",


    "ReplayResultResponse",


    "CostResponse",


    "TokenTelemetryResponse"


]