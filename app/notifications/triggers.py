from app.notifications.enums import (
    NotificationType
)


def determine_notification_type(
    strain_log,
    adaptive_threshold=None
):
    """
    Determines notification type based on
    strain score. Uses adaptive threshold
    from behavioral profile when available.

    The CILIARY_THRESHOLD type fires at the
    adaptive boundary — this is the primary
    "look away now" trigger.
    """

    # Use per-user threshold if available
    threshold = 7
    if adaptive_threshold:
        threshold = adaptive_threshold.get(
            "strain_threshold",
            7
        )

    score = strain_log.strain_score

    # Critical — immediate action required
    if score >= 12:
        return (
            NotificationType.HIGH_STRAIN_ALERT
        )

    # Ciliary threshold reached — the core
    # product trigger: "Look away now."
    if score >= threshold:
        return (
            NotificationType.CILIARY_THRESHOLD
        )

    # Moderate — building strain
    if score >= 4:
        return (
            NotificationType.RECOVERY_SUGGESTION
        )

    # Low — gentle awareness
    if score >= 2:
        return (
            NotificationType.GENTLE_AWARENESS
        )

    return None