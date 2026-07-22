from pydantic import BaseModel, Field





# =====================================================
# TrustOSAI Execution Request Schema
# =====================================================


class ExecutionRequest(BaseModel):


    """
    =====================================================
    Execution API Request

    Supports:

    - Agent Registry Binding
    - Task Execution
    - AI Governance Pipeline

    Example:

    {
        "task": "Analyze security risk",

        "agent_id": 1
    }

    =====================================================
    """



    # -------------------------------------------------
    # User Task
    # -------------------------------------------------


    task: str = Field(

        ...,

        description="Task to execute"

    )





    # -------------------------------------------------
    # Agent Registry Reference
    # -------------------------------------------------


    agent_id: int | None = Field(

        default=None,

        description="Registered TrustOSAI Agent ID"

    )





    # -------------------------------------------------
    # Optional Runtime Parameters
    # -------------------------------------------------


    provider: str | None = Field(

        default=None,

        description="Override model provider"

    )



    model: str | None = Field(

        default=None,

        description="Override AI model"

    )





    # -------------------------------------------------
    # Execution Metadata
    # -------------------------------------------------


    metadata: dict | None = Field(

        default=None,

        description="Additional execution metadata"

    )