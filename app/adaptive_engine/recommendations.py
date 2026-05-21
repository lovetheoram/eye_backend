def recommend_regulation_mode(
    profile
):

    if (
        profile.focus_profile
        == "deep_focus"
    ):
        return "peripheral"

    if (
        profile.recovery_profile
        == "slow_recovery"
    ):
        return "breathing"

    return "horizon"