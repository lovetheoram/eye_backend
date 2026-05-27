from datetime import datetime, timedelta, timezone

from app.notifications.models import (
    NotificationLog
)


# Workday cadence: ~1 notification per hour
MAX_NOTIFICATIONS_PER_DAY = 8

# Interval for ciliary strain notification checks
COOLDOWN_MINUTES = 30


def can_send_notification(
    db,
    user_id,
    adaptive_threshold=None
):
    """
    Checks whether a notification can be sent.

    Respects:
    1. Daily cap (default 8, ~workday hours)
    2. Per-notification cooldown (default 55min)
    3. Optional adaptive threshold from
       behavioral profile
    """

    now = datetime.now(timezone.utc)

    # Use adaptive cooldown if available,
    # otherwise fall back to default
    cooldown = COOLDOWN_MINUTES
    daily_cap = MAX_NOTIFICATIONS_PER_DAY

    if adaptive_threshold:
        cooldown = adaptive_threshold.get(
            "cooldown_minutes",
            COOLDOWN_MINUTES
        )
        daily_cap = adaptive_threshold.get(
            "daily_cap",
            MAX_NOTIFICATIONS_PER_DAY
        )

    # Check daily cap
    recent_notifications = db.query(
        NotificationLog
    ).filter(
        NotificationLog.user_id == user_id,
        NotificationLog.created_at >= (
            now - timedelta(hours=24)
        )
    ).all()

    if (
        len(recent_notifications)
        >= daily_cap
    ):
        return False

    # Check cooldown since last notification
    latest = db.query(
        NotificationLog
    ).filter(
        NotificationLog.user_id == user_id
    ).order_by(
        NotificationLog.created_at.desc()
    ).first()

    if latest:

        if latest.created_at >= (
            now - timedelta(
                minutes=cooldown
            )
        ):
            return False

    return True