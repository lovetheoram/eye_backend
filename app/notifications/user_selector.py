from datetime import datetime, timedelta

from app.auth.models import User
from app.telemetry.models import TelemetryLog


NOTIFICATION_DELAY_MINUTES = 1


def get_active_users(db):
    """
    Get users whose latest telemetry
    is older than X minutes
    """

    now = datetime.utcnow()

    target_cutoff = (
        now - timedelta(
            minutes=NOTIFICATION_DELAY_MINUTES
        )
    )

    return (
        db.query(User)
        .join(TelemetryLog)
        .filter(
            TelemetryLog.created_at
            <= target_cutoff
        )
        .distinct()
        .all()
    )