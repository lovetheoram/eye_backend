import logging

from app.notifications.models import NotificationLog
from app.notifications.cooldowns import can_send_notification
from app.notifications.triggers import determine_notification_type
from app.notifications.templates import generate_message
from app.notifications.delivery import deliver_notification
from app.auth.models import User

logger = logging.getLogger(__name__)


def process_notification(
    db,
    strain_log,
    adaptive_threshold=None
):
    """
    Process and deliver a notification based
    on strain state. Respects cooldown limits
    and uses adaptive thresholds when available.
    """

    if not can_send_notification(
        db,
        strain_log.user_id,
        adaptive_threshold=adaptive_threshold
    ):
        return None

    notification_type = (
        determine_notification_type(
            strain_log,
            adaptive_threshold=adaptive_threshold
        )
    )

    if not notification_type:
        return None

    message = generate_message(
        notification_type
    )

    user = db.query(User).filter(
        User.id == strain_log.user_id
    ).first()

    if not user:
        logger.error(
            "notification_skipped: user not found",
            extra={
                "user_id": str(strain_log.user_id)
            }
        )
        return None

    if not user.expo_push_token:
        logger.debug(
            "notification_skipped: no push token",
            extra={
                "user_id": str(user.id)
            }
        )
        return None

    delivered = deliver_notification(
        expo_push_token=user.expo_push_token,
        message=message,
        notification_type=notification_type
    )

    notification = NotificationLog(
        user_id=strain_log.user_id,
        strain_log_id=strain_log.id,
        notification_type=(
            notification_type.value
        ),
        message=message,
        delivered=delivered
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification