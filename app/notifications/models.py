import uuid

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Boolean
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func

from app.core.database import Base


class NotificationLog(Base):

    __tablename__ = "notification_logs"

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
        nullable=False
    )

    notification_type = Column(
        String,
        nullable=False
    )

    message = Column(
        String,
        nullable=False
    )

    delivered = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )