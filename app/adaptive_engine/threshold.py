def calculate_adaptive_threshold(
    focus_profile,
    recovery_profile
):

    threshold = 7

    if focus_profile == "deep_focus":
        threshold += 2

    if recovery_profile == (
        "slow_recovery"
    ):
        threshold -= 2

    return max(threshold, 3)