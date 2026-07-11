from sqlalchemy import Column, Integer, String, Float, DateTime
from database.connection import Base
from datetime import datetime


class Execution(Base):

    __tablename__ = "executions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    task = Column(
        String,
        nullable=False
    )

    agent = Column(
        String
    )

    trust_score = Column(
        Float
    )

    risk_score = Column(
        Float
    )

    conflict_score = Column(
        Float
    )

    decision = Column(
        String
    )

    result = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )