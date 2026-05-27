import logging

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.donations.models import (
    DonationPrompt,
    DonationConfig
)

from app.streaks.milestones import (
    get_milestone_message
)

logger = logging.getLogger(__name__)


def create_donation_prompt(
    db: Session,
    user_id,
    milestone: int
):
    """
    Creates a donation prompt for a
    streak milestone.
    """

    prompt = DonationPrompt(
        user_id=user_id,
        streak_milestone=milestone
    )

    db.add(prompt)
    db.commit()
    db.refresh(prompt)

    logger.info(
        "donation_prompt_created",
        extra={
            "user_id": str(user_id),
            "milestone": milestone,
            "prompt_id": str(prompt.id)
        }
    )

    return prompt


def log_donation_action(
    db: Session,
    prompt_id,
    action_taken: str
):
    """
    Logs the user's response to a
    donation prompt.

    Valid actions:
      - "dismissed"
      - "opened_gpay"
      - "opened_phonepe"
      - "opened_paytm"
    """

    prompt = db.query(
        DonationPrompt
    ).filter(
        DonationPrompt.id == prompt_id
    ).first()

    if not prompt:
        return None

    prompt.action_taken = action_taken
    prompt.acted_at = (
        datetime.now(timezone.utc)
    )

    db.commit()
    db.refresh(prompt)

    logger.info(
        "donation_action_logged",
        extra={
            "prompt_id": str(prompt_id),
            "action": action_taken
        }
    )

    return prompt


def get_payment_configs(
    db: Session
):
    """
    Returns all active payment configs.
    These are server-managed — can be
    updated without an app release.
    """

    configs = db.query(
        DonationConfig
    ).filter(
        DonationConfig.active == True
    ).order_by(
        DonationConfig.display_order
    ).all()

    return configs


def get_donation_prompt_with_config(
    db: Session,
    user_id,
    milestone: int
):
    """
    Creates a donation prompt and returns
    it with active payment configs.
    """

    prompt = create_donation_prompt(
        db=db,
        user_id=user_id,
        milestone=milestone
    )

    configs = get_payment_configs(db)

    message = get_milestone_message(milestone)

    return {
        "prompt_id": str(prompt.id),
        "milestone": milestone,
        "message": message,
        "payment_options": [
            {
                "payment_app": c.payment_app,
                "display_name": c.display_name,
                "deep_link_template": (
                    c.deep_link_template
                ),
                "upi_id": c.upi_id,
                "suggested_amounts": (
                    c.suggested_amounts
                ),
                "icon_name": c.icon_name
            }
            for c in configs
        ]
    }
