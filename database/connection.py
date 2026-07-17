# database/connection.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# ==================================================
# PostgreSQL Configuration
# ==================================================

DATABASE_URL = (
    "postgresql://trustos:trustos123@localhost:5432/trustos_db"
)


# ==================================================
# SQLAlchemy Engine
# ==================================================

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300
)


# ==================================================
# Session Factory
# ==================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ==================================================
# Declarative Base
# ==================================================

Base = declarative_base()


# ==================================================
# FastAPI Dependency
# Database Session Injection
# ==================================================

def get_db():
    """
    FastAPI database dependency.

    Usage:

    @router.post("/execution/")
    def execute_task(
        db: Session = Depends(get_db)
    ):
        ...
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()