import logging

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.streaks.models import UserStreak

from app.streaks.milestones import (
    check_milestone,
    get_milestone_message
)

logger = logging.getLogger(__name__)

# Streak resets if no completion in 24 hours
STREAK_RESET_HOURS = 24


def get_or_create_streak(
    db: Session,
    user_id
):
    """
    Gets the user's streak record, or
    creates one if it doesn't exist.
    """

    streak = db.query(
        UserStreak
    ).filter(
        UserStreak.user_id == user_id
    ).first()

    if not streak:
        streak = UserStreak(
            user_id=user_id,
            current_streak=0,
            longest_streak=0,
            total_completions=0,
            last_milestone_shown=0
        )

        db.add(streak)
        db.commit()
        db.refresh(streak)

    return streak


def record_completion(
    db: Session,
    user_id
):
    """
    Called after a validated focal isolation
    session. Increments streak or resets if
    gap exceeds threshold.

    Returns dict with streak data and
    optional milestone info.
    """

    streak = get_or_create_streak(
        db, user_id
    )

    now = datetime.now(timezone.utc)

    # Check if streak should reset
    if streak.last_completion_at:

        gap = now - streak.last_completion_at

        if gap > timedelta(
            hours=STREAK_RESET_HOURS
        ):
            # Streak broken
            logger.info(
                "streak_reset",
                extra={
                    "user_id": str(user_id),
                    "previous_streak": (
                        streak.current_streak
                    ),
                    "gap_hours": (
                        gap.total_seconds() / 3600
                    )
                }
            )

            streak.streak_broken_at = now
            streak.current_streak = 0

    # Increment
    streak.current_streak += 1
    streak.total_completions += 1
    streak.last_completion_at = now

    # Update longest if beaten
    if (
        streak.current_streak
        > streak.longest_streak
    ):
        streak.longest_streak = (
            streak.current_streak
        )

    # Check for milestone
    milestone = check_milestone(
        current_streak=streak.current_streak,
        last_milestone_shown=(
            streak.last_milestone_shown
        )
    )

    milestone_data = None

    if milestone:
        streak.last_milestone_shown = milestone

        milestone_data = {
            "milestone": milestone,
            "message": (
                get_milestone_message(milestone)
            ),
            "show_donation": milestone >= 7
        }

        logger.info(
            "streak_milestone_reached",
            extra={
                "user_id": str(user_id),
                "milestone": milestone,
                "current_streak": (
                    streak.current_streak
                )
            }
        )

    db.commit()
    db.refresh(streak)

    return {
        "streak": streak,
        "milestone": milestone_data
    }


def get_user_streak(
    db: Session,
    user_id
):
    """
    Returns the user's current streak data.
    Checks if streak should have expired
    since last completion.
    """

    streak = get_or_create_streak(
        db, user_id
    )

    now = datetime.now(timezone.utc)

    # Check for expired streak
    if (
        streak.last_completion_at
        and streak.current_streak > 0
    ):

        gap = now - streak.last_completion_at

        if gap > timedelta(
            hours=STREAK_RESET_HOURS
        ):
            streak.streak_broken_at = now
            streak.current_streak = 0
            db.commit()
            db.refresh(streak)

    return streak
