from app.notifications.enums import (
    NotificationType
)


def determine_notification_type(
    strain_log
):

    if strain_log.strain_score >= 12:
        return (
            NotificationType.HIGH_STRAIN_ALERT
        )

    if strain_log.strain_score >= 7:
        return (
            NotificationType.RECOVERY_SUGGESTION
        )

    if strain_log.strain_score >= 0:
        return (
            NotificationType.GENTLE_AWARENESS
        )

    return None