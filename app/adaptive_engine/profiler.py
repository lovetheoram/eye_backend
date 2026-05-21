from app.adaptive_engine.enums import (
    FocusProfile,
    RecoveryProfile
)


def determine_focus_profile(
    avg_focus_duration
):

    if avg_focus_duration < 45:
        return (
            FocusProfile.SHORT_CYCLE
        )

    if avg_focus_duration < 120:
        return (
            FocusProfile.BALANCED
        )

    return (
        FocusProfile.DEEP_FOCUS
    )


def determine_recovery_profile(
    avg_recovery_delta
):

    if avg_recovery_delta >= 4:
        return (
            RecoveryProfile
            .FAST_RECOVERY
        )

    if avg_recovery_delta >= 2:
        return (
            RecoveryProfile
            .MODERATE_RECOVERY
        )

    return (
        RecoveryProfile
        .SLOW_RECOVERY
    )