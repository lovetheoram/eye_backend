import uuid

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    DateTime,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func

from app.core.database import Base


class BehavioralProfile(Base):

    __tablename__ = (
        "behavioral_profiles"
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    focus_profile = Column(
        String,
        nullable=True
    )

    recovery_profile = Column(
        String,
        nullable=True
    )

    avg_focus_duration = Column(
        Integer,
        default=0
    )

    avg_recovery_delta = Column(
        Float,
        default=0
    )

    adaptive_strain_threshold = Column(
        Integer,
        default=7
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )