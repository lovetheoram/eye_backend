def determine_emotional_tone(
    strain_level,
    recovery_profile
):

    if strain_level == "high":
        return "gentle"

    if recovery_profile == (
        "slow_recovery"
    ):
        return "supportive"

    return "reflective"