def build_behavioral_context(
    profile,
    latest_insight,
    recent_recovery
):

    return {

        "focus_profile":
        profile.focus_profile,

        "recovery_profile":
        profile.recovery_profile,

        "latest_insight":
        latest_insight.message,

        "recent_recovery":
        recent_recovery.recovery_status
    }