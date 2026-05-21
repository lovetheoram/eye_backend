from app.recovery_engine.enums import (
    RecoveryStatus
)


def compare_recovery(
    pre_score: int,
    post_score: int
):

    delta = (
        pre_score - post_score
    )

    if delta > 1:
        status = (
            RecoveryStatus.IMPROVED
        )

    elif delta == 0:
        status = (
            RecoveryStatus.STABLE
        )

    else:
        status = (
            RecoveryStatus.WORSENED
        )

    return {
        "delta": delta,
        "status": status
    }