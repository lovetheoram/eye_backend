import uuid

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
    Boolean
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func

from app.core.database import Base


class FocalIsolationSession(Base):

    __tablename__ = "focal_isolation_sessions"

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

    notification_id = Column(
        UUID(as_uuid=True),
        ForeignKey("notification_logs.id"),
        nullable=True
    )

    # Dot pattern configuration
    pattern_type = Column(
        String,
        nullable=False,
        default="linear"
    )

    dot_color = Column(
        String,
        nullable=False,
        default="#FF6600"
    )

    duration_ms = Column(
        Integer,
        nullable=False,
        default=20000
    )

    # Session integrity tracking
    started_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    client_frame_count = Column(
        Integer,
        nullable=True
    )

    expected_frame_count = Column(
        Integer,
        nullable=False,
        default=1200
    )

    integrity_score = Column(
        Float,
        nullable=True
    )

    # Outcome
    status = Column(
        String,
        nullable=False,
        default="active"
    )

    completed = Column(
        Boolean,
        default=False
    )

    skipped = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
