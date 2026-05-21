from enum import Enum


class NotificationType(str, Enum):

    GENTLE_AWARENESS = (
        "gentle_awareness"
    )

    RECOVERY_SUGGESTION = (
        "recovery_suggestion"
    )

    HIGH_STRAIN_ALERT = (
        "high_strain_alert"
    )