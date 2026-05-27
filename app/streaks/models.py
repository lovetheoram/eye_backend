import uuid

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func

from app.core.database import Base


class UserStreak(Base):

    __tablename__ = "user_streaks"

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

    # Current consecutive completions
    current_streak = Column(
        Integer,
        nullable=False,
        default=0
    )

    # All-time best
    longest_streak = Column(
        Integer,
        nullable=False,
        default=0
    )

    # Lifetime total completions
    total_completions = Column(
        Integer,
        nullable=False,
        default=0
    )

    # Last successful completion
    last_completion_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # When the streak was last broken
    streak_broken_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # Last milestone shown to user
    last_milestone_shown = Column(
        Integer,
        nullable=False,
        default=0
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
