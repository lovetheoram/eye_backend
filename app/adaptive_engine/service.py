from sqlalchemy.orm import Session

from app.adaptive_engine.models import (
    BehavioralProfile
)

from app.adaptive_engine.memory import (
    calculate_average_focus,
    calculate_average_recovery
)

from app.adaptive_engine.profiler import (
    determine_focus_profile,
    determine_recovery_profile
)

from app.adaptive_engine.threshold import (
    calculate_adaptive_threshold
)


def build_behavioral_profile(
    db: Session,
    user_id,
    telemetry_logs,
    recovery_logs
):

    avg_focus = calculate_average_focus(
        telemetry_logs
    )

    avg_recovery = (
        calculate_average_recovery(
            recovery_logs
        )
    )

    focus_profile = (
        determine_focus_profile(
            avg_focus
        )
    )

    recovery_profile = (
        determine_recovery_profile(
            avg_recovery
        )
    )

    adaptive_threshold = (
        calculate_adaptive_threshold(
            focus_profile.value,
            recovery_profile.value
        )
    )

    profile = db.query(
        BehavioralProfile
    ).filter(
        BehavioralProfile.user_id
        == user_id
    ).first()

    if not profile:

        profile = BehavioralProfile(
            user_id=user_id
        )

    profile.focus_profile = (
        focus_profile.value
    )

    profile.recovery_profile = (
        recovery_profile.value
    )

    profile.avg_focus_duration = (
        avg_focus
    )

    profile.avg_recovery_delta = (
        avg_recovery
    )

    profile.adaptive_strain_threshold = (
        adaptive_threshold
    )

    db.add(profile)

    db.commit()

    db.refresh(profile)

    return profile