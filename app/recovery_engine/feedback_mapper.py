from app.recovery_engine.enums import (
    RecoveryStatus
)


def map_feedback_to_scores(
    pre_score: int,
    feedback: str
):

    feedback = feedback.lower()

    if feedback == "better":

        post_score = max(
            pre_score - 2,
            0
        )

        status = (
            RecoveryStatus.IMPROVED
        )

    elif feedback == "same":

        post_score = pre_score

        status = (
            RecoveryStatus.STABLE
        )

    else:

        post_score = pre_score + 1

        status = (
            RecoveryStatus.WORSENED
        )

    delta = (
        pre_score - post_score
    )

    return {

        "post_score": post_score,

        "delta": delta,

        "status": status
    }