from enum import Enum


class BehavioralContext(str, Enum):

    DEEP_FOCUS = "deep_focus"

    FRAGMENTED_ATTENTION = (
        "fragmented_attention"
    )

    PASSIVE_SCROLLING = (
        "passive_scrolling"
    )

    LATE_NIGHT_STRAIN = (
        "late_night_strain"
    )

    VISUAL_OVERLOAD = (
        "visual_overload"
    )

    RECOVERY_FRIENDLY = (
        "recovery_friendly"
    )