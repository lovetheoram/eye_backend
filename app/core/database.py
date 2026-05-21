from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings


# engine = create_engine(settings.DATABASE_URL)
from sqlalchemy import create_engine

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # ✅ checks connection before using
    pool_recycle=300      # ✅ refresh every 5 minutes
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()