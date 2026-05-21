from datetime import datetime, timedelta

from app.notifications.models import (
    NotificationLog
)


MAX_NOTIFICATIONS_PER_DAY = 3

COOLDOWN_HOURS = 2


def can_send_notification(
    db,
    user_id
):

    now = datetime.utcnow()

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
        >= MAX_NOTIFICATIONS_PER_DAY
    ):
        return False

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
                hours=COOLDOWN_HOURS
            )
        ):
            return False

    return True