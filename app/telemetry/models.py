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


class TelemetryLog(Base):
    __tablename__ = "telemetry_logs"

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

    app_name = Column(String, nullable=False)

    app_category = Column(String, nullable=False)

    screen_on_minutes = Column(Integer, nullable=False)

    continuous_focus_minutes = Column(
        Integer,
        nullable=False
    )

    brightness_level = Column(Integer, nullable=False)

    session_count = Column(Integer, nullable=False)

    time_of_day = Column(String, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )