from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


DATABASE_URL = "postgresql://trustos:trustos123@localhost:5432/trustos_db"


engine = create_engine(
    DATABASE_URL,
    echo=True
)


Base = declarative_base()