from app.notifications.enums import (
    NotificationType
)


def generate_message(
    notification_type
):

    templates = {

        NotificationType.GENTLE_AWARENESS:
        (
            "Your visual focus has "
            "remained steady for a while."
        ),

        NotificationType.RECOVERY_SUGGESTION:
        (
            "A softer visual reset "
            "may help your eyes relax."
        ),

        NotificationType.HIGH_STRAIN_ALERT:
        (
            "Your visual rhythm appears "
            "intense tonight."
        )
    }

    return templates.get(
        notification_type,
        "Take a moment to reset."
    )