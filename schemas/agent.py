from datetime import datetime

from typing import Any, Dict, Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)





# =====================================================
# AGENT MEMORY CONFIGURATION
# =====================================================


class AgentMemoryConfigSchema(BaseModel):

    """
    TrustOSAI Agent Memory Runtime Configuration
    """

    enabled: bool = Field(
        default=True
    )


    memory_type: str = Field(
        default="LONG_TERM",
        max_length=50
    )


    max_context_tokens: int = Field(
        default=8000,
        ge=1000
    )


    retention_days: int = Field(
        default=365,
        ge=1
    )


    model_config = ConfigDict(
        from_attributes=True
    )









# =====================================================
# CREATE AGENT REQUEST
# =====================================================


class AgentCreate(BaseModel):


    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )


    description: Optional[str] = None



    agent_type: str = Field(
        default="GENERAL",
        max_length=50
    )



    model: str = Field(
        ...,
        min_length=2,
        max_length=100
    )



    provider: str = Field(
        default="local",
        max_length=50
    )



    trust_threshold: float = Field(
        default=60.0,
        ge=0,
        le=100
    )



    risk_level: str = Field(
        default="MEDIUM",
        max_length=50
    )



    status: str = Field(
        default="ACTIVE",
        max_length=50
    )



    metadata_json: Optional[Dict[str,Any]] = Field(
        default_factory=dict
    )



    memory: Optional[
        AgentMemoryConfigSchema
    ] = None



    model_config = ConfigDict(
        from_attributes=True
    )









# =====================================================
# UPDATE AGENT
# =====================================================


class AgentUpdate(BaseModel):


    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )


    description: Optional[str] = None



    agent_type: Optional[str] = None



    model: Optional[str] = None



    provider: Optional[str] = None



    trust_threshold: Optional[float] = Field(
        default=None,
        ge=0,
        le=100
    )



    risk_level: Optional[str] = None



    status: Optional[str] = None



    metadata_json: Optional[
        Dict[str,Any]
    ] = None



    memory: Optional[
        AgentMemoryConfigSchema
    ] = None



    model_config = ConfigDict(
        from_attributes=True
    )









# =====================================================
# MEMORY RESPONSE
# =====================================================


class AgentMemoryResponse(BaseModel):


    id:int


    agent_id:int


    enabled:bool


    memory_type:str


    max_context_tokens:int


    retention_days:int


    created_at:datetime


    updated_at:Optional[datetime]=None



    model_config = ConfigDict(
        from_attributes=True
    )









# =====================================================
# AGENT RESPONSE
# =====================================================


class AgentResponse(BaseModel):


    id:int


    name:str



    description:Optional[str]=None



    agent_type:str



    model:str



    provider:str



    trust_threshold:float



    risk_level:str



    status:str



    total_executions:int



    average_trust:float



    metadata_json:Optional[
        Dict[str,Any]
    ] = None



    # ==========================================
    # IMPORTANT FIX
    #
    # SQLAlchemy:
    # Agent.memory_config
    #
    # API:
    # memory
    #
    # ==========================================


    memory: Optional[
        AgentMemoryResponse
    ] = Field(
        default=None,
        validation_alias="memory_config",
        serialization_alias="memory"
    )



    created_at:datetime



    updated_at:Optional[datetime]=None



    model_config = ConfigDict(

        from_attributes=True,

        populate_by_name=True

    )









# =====================================================
# AGENT DETAIL RESPONSE
# =====================================================


class AgentDetailResponse(
    AgentResponse
):


    memory_count:int = 0


    last_execution_at:Optional[
        datetime
    ] = None









# =====================================================
# AGENT STATISTICS RESPONSE
# =====================================================


class AgentStatsResponse(BaseModel):


    agent_id:int


    agent_name:str


    model:str


    provider:str


    status:str


    total_executions:int


    average_trust:float


    success_rate:float = 0.0


    blocked_count:int = 0


    average_latency_ms:float = 0.0


    total_cost_usd:float = 0.0


    memory_count:int = 0



    model_config = ConfigDict(
        from_attributes=True
    )