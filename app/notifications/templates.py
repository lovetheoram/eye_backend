from app.notifications.enums import (
    NotificationType
)


def generate_message(
    notification_type
):
    """
    Bold, direct notification copy.

    These messages are designed to feel
    urgent and authoritative — not passive.
    The user should feel compelled to act
    immediately.
    """

    templates = {

        NotificationType.CILIARY_THRESHOLD:
        (
            "Ciliary muscle strain threshold "
            "reached. Look away now."
        ),

        NotificationType.HIGH_STRAIN_ALERT:
        (
            "Your eyes have been locked "
            "for too long. 20-second "
            "reset incoming."
        ),

        NotificationType.RECOVERY_SUGGESTION:
        (
            "Your focus pattern is "
            "building strain. Quick reset?"
        ),

        NotificationType.GENTLE_AWARENESS:
        (
            "Your visual focus has held "
            "steady for a while. Time "
            "to break the lock."
        ),

        NotificationType.STREAK_MILESTONE:
        (
            "You just hit a new streak "
            "milestone. Your eyes thank you."
        ),

        NotificationType.GRATITUDE_PROMPT:
        (
            "Your eye health streak is "
            "going strong. Want to pay "
            "it forward?"
        )
    }

    return templates.get(
        notification_type,
        "Your eyes need a reset. Act now."
    )


def generate_title(
    notification_type
):
    """
    Notification title — shown as the
    bold header on the push notification.
    """

    titles = {

        NotificationType.CILIARY_THRESHOLD:
            "⚠️ Eye Strain Alert",

        NotificationType.HIGH_STRAIN_ALERT:
            "🔴 Strain Critical",

        NotificationType.RECOVERY_SUGGESTION:
            "👁️ Quick Reset",

        NotificationType.GENTLE_AWARENESS:
            "👁️ Focus Check",

        NotificationType.STREAK_MILESTONE:
            "🔥 Streak Milestone!",

        NotificationType.GRATITUDE_PROMPT:
            "💙 Pay It Forward"
    }

    return titles.get(
        notification_type,
        "👁️ Eye Buddy"
    )