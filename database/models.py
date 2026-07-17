from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text
)

from database.connection import Base


class Execution(Base):
    """
    TrustOSAI Execution Runtime Database Model

    Stores:
    - Agent execution requests
    - Trust governance decisions
    - Risk/conflict evaluation
    - Runtime telemetry
    - LLM usage metrics
    """

    __tablename__ = "executions"


    # =====================================
    # Primary Identifier
    # =====================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # =====================================
    # Execution Input
    # =====================================

    task = Column(
        String,
        nullable=False
    )


    agent = Column(
        String,
        nullable=True
    )


    # =====================================
    # Trust Governance Layer
    # =====================================

    trust_score = Column(
        Float,
        default=0.0,
        nullable=False
    )


    risk_score = Column(
        Float,
        default=0.0,
        nullable=False
    )


    conflict_score = Column(
        Float,
        default=0.0,
        nullable=False
    )


    decision = Column(
        String,
        nullable=True
    )


    # =====================================
    # Execution Result
    # =====================================

    result = Column(
        Text,
        nullable=True
    )


    # =====================================
    # TrustOSAI v3 Runtime Telemetry Layer
    # =====================================

    quality_score = Column(
        Float,
        default=0.0,
        nullable=False
    )


    latency_ms = Column(
        Float,
        default=0.0,
        nullable=False
    )


    # =====================================
    # LLM Cost / Usage Attribution Layer
    # =====================================

    prompt_tokens = Column(
        Integer,
        default=0,
        nullable=False
    )


    completion_tokens = Column(
        Integer,
        default=0,
        nullable=False
    )


    # =====================================
    # Timestamp
    # =====================================

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    def __repr__(self):
        return (
            f"<Execution "
            f"id={self.id} "
            f"task='{self.task}' "
            f"decision='{self.decision}' "
            f"trust={self.trust_score}>"
        )