from sqlalchemy.orm import Session

from app.regulation.models import (
    RegulationSession
)

from app.regulation.timers import (
    validate_duration
)


def create_regulation_session(
    db: Session,
    user_id,
    payload
):

    if not validate_duration(
        payload.duration_seconds
    ):
        raise ValueError(
            "Invalid duration"
        )

    session = RegulationSession(

        user_id=user_id,

        strain_log_id=(
            payload.strain_log_id
        ),

        mode=payload.mode.value,

        duration_seconds=(
            payload.duration_seconds
        ),

        completed=False
    )

    db.add(session)

    db.commit()

    db.refresh(session)

    return session


def complete_regulation_session(
    db: Session,
    session
):

    session.completed = True

    db.commit()

    db.refresh(session)

    return session