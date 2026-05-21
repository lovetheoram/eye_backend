import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func

from app.core.database import Base


class RecoveryLog(Base):

    __tablename__ = "recovery_logs"

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

    regulation_session_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "regulation_sessions.id"
        ),
        nullable=False
    )

    pre_strain_score = Column(
        Integer,
        nullable=False
    )

    post_strain_score = Column(
        Integer,
        nullable=False
    )

    recovery_delta = Column(
        Integer,
        nullable=False
    )

    recovery_status = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )