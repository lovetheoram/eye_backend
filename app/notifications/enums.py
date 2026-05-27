from enum import Enum


class NotificationType(str, Enum):

    # Existing — soft awareness
    GENTLE_AWARENESS = (
        "gentle_awareness"
    )

    RECOVERY_SUGGESTION = (
        "recovery_suggestion"
    )

    HIGH_STRAIN_ALERT = (
        "high_strain_alert"
    )

    # New — vision-aligned urgent types
    CILIARY_THRESHOLD = (
        "ciliary_threshold"
    )

    STREAK_MILESTONE = (
        "streak_milestone"
    )

    GRATITUDE_PROMPT = (
        "gratitude_prompt"
    )