def generate_behavioral_reflection(
    profile,
    latest_insight
):

    if (
        profile.focus_profile
        == "deep_focus"
    ):

        return (
            "Your attention appears "
            "deeply immersive lately. "
            "Moments of visual distance "
            "may help your system settle."
        )

    return (
        latest_insight.message
    )