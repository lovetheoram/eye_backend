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
    pre_score = 0
    strain = None
    regulation_session_id = None
    focal_isolation_session_id = None

    if payload.regulation_session_id:
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
        regulation_session_id = session.id
        if session.strain_log_id:
            strain = db.query(StrainLog).filter(StrainLog.id == session.strain_log_id).first()
    elif payload.focal_isolation_session_id:
        from app.focal_isolation.models import FocalIsolationSession
        session = db.query(
            FocalIsolationSession
        ).filter(
            FocalIsolationSession.id
            == payload.focal_isolation_session_id
        ).first()

        if not session:
            raise ValueError(
                "Invalid focal isolation session"
            )
        focal_isolation_session_id = session.id
        if session.strain_log_id:
            strain = db.query(StrainLog).filter(StrainLog.id == session.strain_log_id).first()
    else:
        raise ValueError("Must provide either regulation_session_id or focal_isolation_session_id")

    if not strain:
        # Fallback to the user's latest strain log
        strain = db.query(
            StrainLog
        ).filter(
            StrainLog.user_id == user_id
        ).order_by(
            StrainLog.created_at.desc()
        ).first()

    if strain:
        pre_score = strain.strain_score

    result = map_feedback_to_scores(
        pre_score=pre_score,
        feedback=payload.feedback
    )

    # Check if a recovery log already exists for this session to update it instead of creating duplicates
    recovery_log = None
    if focal_isolation_session_id:
        recovery_log = db.query(RecoveryLog).filter(
            RecoveryLog.focal_isolation_session_id == focal_isolation_session_id
        ).first()
    elif regulation_session_id:
        recovery_log = db.query(RecoveryLog).filter(
            RecoveryLog.regulation_session_id == regulation_session_id
        ).first()

    if recovery_log:
        recovery_log.pre_strain_score = pre_score
        recovery_log.post_strain_score = result["post_score"]
        recovery_log.recovery_delta = result["delta"]
        recovery_log.recovery_status = result["status"].value
    else:
        recovery_log = RecoveryLog(
            user_id=user_id,
            regulation_session_id=regulation_session_id,
            focal_isolation_session_id=focal_isolation_session_id,
            pre_strain_score=pre_score,
            post_strain_score=result["post_score"],
            recovery_delta=result["delta"],
            recovery_status=result["status"].value
        )
        db.add(recovery_log)

    db.commit()
    db.refresh(recovery_log)

    return recovery_log