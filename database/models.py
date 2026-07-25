from datetime import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    JSON,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import relationship

from database.connection import Base



# =====================================================
# AGENT REGISTRY
# =====================================================


class Agent(Base):

    __tablename__ = "agents"


    id = Column(
        BigInteger,
        primary_key=True,
        index=True,
        autoincrement=True
    )


    name = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True
    )


    description = Column(
        Text,
        nullable=True
    )


    agent_type = Column(
        String(50),
        default="GENERAL"
    )


    # =================================================
    # MODEL CONFIG
    # =================================================


    model = Column(
        String(100),
        nullable=False,
        default="local"
    )


    provider = Column(
        String(50),
        nullable=False,
        default="local"
    )


    # =================================================
    # GOVERNANCE
    # =================================================


    trust_threshold = Column(
        Float,
        default=60.0
    )


    risk_level = Column(
        String(50),
        default="MEDIUM"
    )


    status = Column(
        String(50),
        default="ACTIVE",
        index=True
    )


    # =================================================
    # ANALYTICS
    # =================================================


    total_executions = Column(
        Integer,
        default=0,
        nullable=False
    )


    average_trust = Column(
        Float,
        default=0.0,
        nullable=False
    )


    metadata_json = Column(
        JSON,
        default=dict
    )


    # =================================================
    # TIMESTAMP
    # =================================================


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )



    # =================================================
    # RELATIONSHIP
    # =================================================


    executions = relationship(
        "Execution",
        back_populates="agent_ref",
        foreign_keys="Execution.agent_id"
    )


    memory_config = relationship(
        "AgentMemoryConfig",
        back_populates="agent",
        uselist=False,
        cascade="all, delete-orphan"
    )


    memories = relationship(
        "AgentMemory",
        back_populates="agent",
        cascade="all, delete-orphan"
    )



    def __repr__(self):

        return (
            f"<Agent id={self.id} "
            f"name={self.name}>"
        )





# =====================================================
# EXECUTION RUNTIME
# =====================================================


class Execution(Base):

    __tablename__ = "executions"



    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )



    task = Column(
        Text,
        nullable=False
    )



    # Display Agent Name

    agent = Column(
        String(100),
        nullable=False
    )



    # REAL FOREIGN KEY

    agent_id = Column(
        BigInteger,
        ForeignKey(
            "agents.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )



    # =================================================
    # ROUTING
    # =================================================


    route = Column(
        String(100),
        nullable=True
    )



    provider = Column(
        String(50),
        default="local"
    )


    model = Column(
        String(100),
        nullable=True
    )



    # =================================================
    # TRUST ENGINE
    # =================================================


    trust_score = Column(
        Float,
        default=0
    )


    risk_score = Column(
        Float,
        default=0
    )


    conflict_score = Column(
        Float,
        default=0
    )



    decision = Column(
        String(50),
        default="REVIEW"
    )



    # =================================================
    # GOVERNANCE ENGINE
    # =================================================


    governance_result = Column(
        Text,
        nullable=True
    )


    governance_reason = Column(
        Text,
        nullable=True
    )


    governance_level = Column(
        String(50),
        default="SAFE"
    )


    governance_status = Column(
        String(50),
        default="APPROVED"
    )


    policy_result = Column(
        String(50),
        nullable=True
    )


    policy_version = Column(
        String(50),
        default="v1.2.0"
    )


    governance_metadata = Column(
        JSON,
        default=dict
    )


    reasoning = Column(
        Text,
        nullable=True
    )



    # =================================================
    # EXECUTION OUTPUT
    # =================================================


    result = Column(
        Text,
        nullable=True
    )


    execution_result = Column(
        Text,
        nullable=True
    )



    # =================================================
    # TELEMETRY
    # =================================================


    runtime_ms = Column(
        Float,
        default=0
    )


    latency_ms = Column(
        Float,
        default=0
    )


    quality_score = Column(
        Float,
        default=0
    )



    prompt_tokens = Column(
        Integer,
        default=0
    )


    completion_tokens = Column(
        Integer,
        default=0
    )


    total_tokens = Column(
        Integer,
        default=0
    )


    tokens_used = Column(
        Integer,
        default=0
    )



    telemetry = Column(
        JSON,
        default=dict
    )


    execution_trace = Column(
        JSON,
        default=dict
    )



    # =================================================
    # COST ATTRIBUTION
    # =================================================


    cost_usd = Column(
        Float,
        default=0
    )


    currency = Column(
        String(10),
        default="USD"
    )



    # =================================================
    # REPLAY ENGINE
    # =================================================


    execution_type = Column(
        String(50),
        default="NORMAL",
        index=True
    )



    parent_execution_id = Column(
        BigInteger,
        ForeignKey(
            "executions.id",
            ondelete="SET NULL"
        ),
        nullable=True,
        index=True
    )



    # =================================================
    # STATUS
    # =================================================


    status = Column(
        String(50),
        default="COMPLETED"
    )



    # =================================================
    # TIMESTAMP
    # =================================================


    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )


    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )



    # =================================================
    # RELATIONSHIP
    # =================================================


    agent_ref = relationship(
        "Agent",
        back_populates="executions",
        foreign_keys=[agent_id]
    )


    parent_execution = relationship(
        "Execution",
        remote_side=[id],
        back_populates="child_executions"
    )


    child_executions = relationship(
        "Execution",
        back_populates="parent_execution"
    )


    memories = relationship(
        "AgentMemory",
        back_populates="execution",
        cascade="all, delete-orphan"
    )



    def __repr__(self):

        return (
            f"<Execution "
            f"id={self.id} "
            f"agent={self.agent}>"
        )







# =====================================================
# AGENT MEMORY CONFIGURATION
# =====================================================


class AgentMemoryConfig(Base):

    __tablename__ = "agent_memory_config"



    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )


    agent_id = Column(
        BigInteger,
        ForeignKey(
            "agents.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        unique=True
    )


    enabled = Column(
        Boolean,
        default=True
    )


    memory_type = Column(
        String(50),
        default="LONG_TERM"
    )


    max_context_tokens = Column(
        Integer,
        default=8000
    )


    retention_days = Column(
        Integer,
        default=365
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    agent = relationship(
        "Agent",
        back_populates="memory_config"
    )







# =====================================================
# LONG TERM MEMORY
# =====================================================


class AgentMemory(Base):

    __tablename__ = "agent_memory"



    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )


    agent_id = Column(
        BigInteger,
        ForeignKey(
            "agents.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )


    execution_id = Column(
        BigInteger,
        ForeignKey(
            "executions.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )


    memory_type = Column(
        String(50),
        default="EXECUTION"
    )


    content = Column(
        Text,
        nullable=False
    )


    importance_score = Column(
        Float,
        default=0.5
    )


    access_count = Column(
        Integer,
        default=0
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )



    agent = relationship(
        "Agent",
        back_populates="memories"
    )


    execution = relationship(
        "Execution",
        back_populates="memories"
    )



    def __repr__(self):

        return (
            f"<AgentMemory "
            f"id={self.id}>"
        )