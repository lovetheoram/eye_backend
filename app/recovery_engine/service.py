from sqlalchemy.orm import Session

from app.recovery_engine.models import (
    RecoveryLog
)

from app.regulation.models import (
    RegulationSession
)

from app.strain_engine.models import (
    StrainLog
)

from app.recovery_engine.feedback_mapper import (
    map_feedback_to_scores
)


def create_recovery_log(
    db: Session,
    user_id,
    payload
):

    """
    Get regulation session
    """

    session = db.query(
        RegulationSession
    ).filter(
        RegulationSession.id
        == payload.regulation_session_id
    ).first()

    if not session:
        raise ValueError(
            "Invalid regulation session"
        )

    """
    Get original strain
    """

    strain = db.query(
        StrainLog
    ).filter(
        StrainLog.id
        == session.strain_log_id
    ).first()

    if not strain:
        raise ValueError(
            "Strain log not found"
        )

    pre_score = (
        strain.strain_score
    )

    """
    Convert feedback into recovery values
    """

    result = map_feedback_to_scores(

        pre_score=pre_score,

        feedback=payload.feedback
    )

    recovery_log = RecoveryLog(

        user_id=user_id,

        regulation_session_id=(
            payload.regulation_session_id
        ),

        pre_strain_score=pre_score,

        post_strain_score=(
            result["post_score"]
        ),

        recovery_delta=(
            result["delta"]
        ),

        recovery_status=(
            result["status"].value
        )
    )

    db.add(recovery_log)

    db.commit()

    db.refresh(recovery_log)

    return recovery_log