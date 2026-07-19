from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Float,
    DateTime,
    Text,
    JSON
)

from database.connection import Base


class Execution(Base):

    __tablename__ = "executions"


    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )


    task = Column(
        Text,
        nullable=False
    )


    agent = Column(
        Text,
        nullable=False
    )


    trust_score = Column(
        Float,
        default=0.0
    )


    risk_score = Column(
        Float,
        default=0.0
    )


    conflict_score = Column(
        Float,
        default=0.0
    )


    decision = Column(
        String,
        nullable=True
    )


    policy_result = Column(
        String,
        nullable=True
    )


    governance_result = Column(
        String,
        nullable=True
    )


    governance_status = Column(
        String,
        nullable=True
    )


    governance_reason = Column(
        Text,
        nullable=True
    )


    route = Column(
        String,
        nullable=True
    )


    result = Column(
        Text,
        nullable=True
    )


    execution_result = Column(
        Text,
        nullable=True
    )


    runtime_ms = Column(
        Float,
        default=0.0
    )


    quality_score = Column(
        Float,
        default=0.0
    )


    latency_ms = Column(
        Float,
        default=0.0
    )


    prompt_tokens = Column(
        Integer,
        default=0
    )


    completion_tokens = Column(
        Integer,
        default=0
    )


    cost_usd = Column(
        Float,
        default=0.0
    )


    execution_trace = Column(
        JSON,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    def __repr__(self):

        return (
            f"<Execution "
            f"id={self.id} "
            f"decision={self.decision} "
            f"trust={self.trust_score}>"
        )