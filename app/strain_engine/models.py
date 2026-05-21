import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func

from app.core.database import Base


class StrainLog(Base):

    __tablename__ = "strain_logs"

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

    telemetry_id = Column(
        UUID(as_uuid=True),
        ForeignKey("telemetry_logs.id"),
        nullable=False
    )

    strain_score = Column(
        Integer,
        nullable=False
    )

    risk_level = Column(
        String,
        nullable=False
    )

    recovery_needed = Column(
        Boolean,
        default=False
    )

    recovery_debt = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )