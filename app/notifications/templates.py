from app.notifications.enums import (
    NotificationType
)


def generate_message(
    notification_type
):
    """
    Focus Endurance System notification copy.

    Designed to feel like intelligent detection,
    not a timer ringing. Users should feel:
    "The app noticed something."
    """

    templates = {

        NotificationType.CILIARY_THRESHOLD:
        (
            "52 minutes of continuous activity "
            "detected. 20-second reset recommended."
        ),

        NotificationType.HIGH_STRAIN_ALERT:
        (
            "You've been in a high-intensity "
            "session. Restore focus now."
        ),

        NotificationType.RECOVERY_SUGGESTION:
        (
            "Quick reset available."
        ),

        NotificationType.GENTLE_AWARENESS:
        (
            "You've been focused for a while. "
            "Quick recharge available."
        ),

        NotificationType.STREAK_MILESTONE:
        (
            "You just hit a new focus streak "
            "milestone. Keep the momentum going."
        ),

        NotificationType.GRATITUDE_PROMPT:
        (
            "Your focus streak is going strong. "
            "Want to support future development?"
        )
    }

    return templates.get(
        notification_type,
        "Focus Battery dropping. Quick recharge available."
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
            "📉 Focus Quality Dropping",

        NotificationType.HIGH_STRAIN_ALERT:
            "⚡ Fatigue Risk Rising",

        NotificationType.RECOVERY_SUGGESTION:
            "⏳ Focus Window Ending",

        NotificationType.GENTLE_AWARENESS:
            "🔋 Focus Battery Low",

        NotificationType.STREAK_MILESTONE:
            "🔥 Streak Milestone!",

        NotificationType.GRATITUDE_PROMPT:
            "💙 Support Eye Buddy"
    }

    return titles.get(
        notification_type,
        "🔋 Eye Buddy"
    )