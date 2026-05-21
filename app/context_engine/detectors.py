from app.context_engine.enums import (
    BehavioralContext
)

from app.context_engine.rules import (
    DEEP_FOCUS_MINUTES,
    HIGH_BRIGHTNESS_LEVEL,
    FRAGMENTED_SESSION_COUNT,
    LATE_NIGHT_FOCUS_MINUTES,
    LOW_SESSION_FRAGMENTATION
)


def detect_contexts(telemetry):

    detected = []

    if (
        telemetry.continuous_focus_minutes
        >= DEEP_FOCUS_MINUTES
    ):
        detected.append(
            BehavioralContext.DEEP_FOCUS
        )

    if (
        telemetry.session_count
        >= FRAGMENTED_SESSION_COUNT
    ):
        detected.append(
            BehavioralContext.FRAGMENTED_ATTENTION
        )

    if (
        telemetry.time_of_day == "night"
        and telemetry.continuous_focus_minutes
        >= LATE_NIGHT_FOCUS_MINUTES
    ):
        detected.append(
            BehavioralContext.LATE_NIGHT_STRAIN
        )

    if (
        telemetry.brightness_level
        >= HIGH_BRIGHTNESS_LEVEL
        and telemetry.continuous_focus_minutes
        >= DEEP_FOCUS_MINUTES
    ):
        detected.append(
            BehavioralContext.VISUAL_OVERLOAD
        )

    if not detected:

        detected.append(
            BehavioralContext.RECOVERY_FRIENDLY
        )

    return detected