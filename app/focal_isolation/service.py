import logging

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.focal_isolation.models import (
    FocalIsolationSession
)

from app.focal_isolation.patterns import (
    get_pattern_config,
    SESSION_DURATION_MS,
    EXPECTED_FRAME_COUNT,
    DEFAULT_DOT_COLOR
)

from app.focal_isolation.validator import (
    validate_completion
)

logger = logging.getLogger(__name__)


def create_session(
    db: Session,
    user_id,
    payload
):
    """
    Creates a new focal isolation session
    and returns the pattern config for
    the client to render.
    """

    config = get_pattern_config(
        payload.pattern_type
    )

    session = FocalIsolationSession(
        user_id=user_id,
        strain_log_id=payload.strain_log_id,
        notification_id=payload.notification_id,
        pattern_type=payload.pattern_type,
        dot_color=DEFAULT_DOT_COLOR,
        duration_ms=SESSION_DURATION_MS,
        expected_frame_count=EXPECTED_FRAME_COUNT,
        started_at=datetime.now(timezone.utc),
        status="active"
    )

    db.add(session)

    db.commit()

    db.refresh(session)

    logger.info(
        "focal_isolation_session_created",
        extra={
            "session_id": str(session.id),
            "user_id": str(user_id),
            "pattern": payload.pattern_type
        }
    )

    return {
        "session": session,
        "config": {
            "session_id": str(session.id),
            **config
        }
    }


def complete_session(
    db: Session,
    session,
    client_report
):
    """
    Validates and completes a focal isolation
    session. Enforces the hard stop — rejects
    fake or too-fast completions.
    """

    validation = validate_completion(
        session=session,
        client_report=client_report
    )

    if not validation["valid"]:
        logger.warning(
            "focal_isolation_completion_rejected",
            extra={
                "session_id": str(session.id),
                "reason": (
                    validation["rejection_reason"]
                )
            }
        )

        return {
            "accepted": False,
            "reason": (
                validation["rejection_reason"]
            ),
            "session": session
        }

    # Mark as completed
    session.completed = True
    session.skipped = False
    session.status = "completed"
    session.completed_at = (
        datetime.now(timezone.utc)
    )
    session.client_frame_count = (
        client_report.client_frame_count
    )
    session.integrity_score = (
        validation["integrity_score"]
    )

    db.commit()

    db.refresh(session)

    logger.info(
        "focal_isolation_session_completed",
        extra={
            "session_id": str(session.id),
            "integrity_score": (
                validation["integrity_score"]
            )
        }
    )

    return {
        "accepted": True,
        "reason": None,
        "session": session
    }


def skip_session(
    db: Session,
    session
):
    """
    Marks a session as skipped by the user.
    Tracked for behavioral analysis — users
    who skip often may need different
    notification strategies.
    """

    session.skipped = True
    session.completed = False
    session.status = "skipped"

    db.commit()

    db.refresh(session)

    logger.info(
        "focal_isolation_session_skipped",
        extra={
            "session_id": str(session.id)
        }
    )

    return session
