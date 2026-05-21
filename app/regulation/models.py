import uuid

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func

from app.core.database import Base


class RegulationSession(Base):

    __tablename__ = (
        "regulation_sessions"
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    strain_log_id = Column(
        UUID(as_uuid=True),
        ForeignKey("strain_logs.id"),
        nullable=True
    )

    mode = Column(
        String,
        nullable=False
    )

    duration_seconds = Column(
        Integer,
        nullable=False
    )

    completed = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )