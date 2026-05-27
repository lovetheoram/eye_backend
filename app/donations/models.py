import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import (
    UUID,
    ARRAY
)

from sqlalchemy.sql import func

from app.core.database import Base


class DonationPrompt(Base):

    __tablename__ = "donation_prompts"

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

    # Which milestone triggered this
    streak_milestone = Column(
        Integer,
        nullable=False
    )

    shown_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # User response tracking
    action_taken = Column(
        String,
        nullable=True
    )

    acted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class DonationConfig(Base):
    """
    Server-managed payment deep links.
    Updateable without app release.
    """

    __tablename__ = "donation_configs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    payment_app = Column(
        String,
        nullable=False
    )

    display_name = Column(
        String,
        nullable=False
    )

    deep_link_template = Column(
        String,
        nullable=False
    )

    upi_id = Column(
        String,
        nullable=True
    )

    suggested_amounts = Column(
        String,
        nullable=False,
        default="10,25,50"
    )

    icon_name = Column(
        String,
        nullable=True
    )

    active = Column(
        Boolean,
        default=True
    )

    display_order = Column(
        Integer,
        default=0
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
