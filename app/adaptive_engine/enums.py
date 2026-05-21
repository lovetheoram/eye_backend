from enum import Enum


class FocusProfile(str, Enum):

    SHORT_CYCLE = "short_cycle"

    BALANCED = "balanced"

    DEEP_FOCUS = "deep_focus"


class RecoveryProfile(str, Enum):

    FAST_RECOVERY = "fast_recovery"

    MODERATE_RECOVERY = (
        "moderate_recovery"
    )

    SLOW_RECOVERY = "slow_recovery"