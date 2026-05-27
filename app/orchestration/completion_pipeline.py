"""
Completion pipeline.

Orchestrates the post-session flow:
  focal isolation complete
    → validate integrity
    → log recovery
    → update streak
    → check milestone
    → maybe trigger donation prompt

This is the second pipeline, complementing
the existing behavioral_pipeline.py which
handles the input/detection side.
"""

import logging

from sqlalchemy.orm import Session

from app.focal_isolation.models import (
    FocalIsolationSession
)

from app.focal_isolation.service import (
    complete_session
)

from app.streaks.service import (
    record_completion
)

from app.recovery_engine.models import (
    RecoveryLog
)

logger = logging.getLogger(__name__)


def process_session_completion(
    db: Session,
    user_id,
    session_id,
    client_report
):
    """
    Full completion flow triggered when
    the client reports a focal isolation
    session is finished.

    Returns a unified response with session
    status, streak data, and optional
    milestone/donation info.
    """

    # 1. Find the session
    session = db.query(
        FocalIsolationSession
    ).filter(
        FocalIsolationSession.id
        == session_id,
        FocalIsolationSession.user_id
        == user_id
    ).first()

    if not session:
        return {
            "success": False,
            "error": "session_not_found"
        }

    # 2. Validate and complete session
    result = complete_session(
        db=db,
        session=session,
        client_report=client_report
    )

    if not result["accepted"]:
        return {
            "success": False,
            "error": result["reason"],
            "session_status": "rejected"
        }

    # 3. Create recovery log
    recovery_log = RecoveryLog(
        user_id=user_id,
        regulation_session_id=None,
        pre_strain_score=(
            _get_pre_strain_score(
                db, session
            )
        ),
        post_strain_score=0,
        recovery_delta=0,
        recovery_status="completed"
    )

    db.add(recovery_log)
    db.commit()

    # 4. Update streak
    streak_result = record_completion(
        db=db,
        user_id=user_id
    )

    # 5. Build response
    response = {
        "success": True,
        "session_status": "completed",
        "integrity_score": (
            session.integrity_score
        ),
        "streak": {
            "current": (
                streak_result["streak"]
                .current_streak
            ),
            "longest": (
                streak_result["streak"]
                .longest_streak
            ),
            "total_completions": (
                streak_result["streak"]
                .total_completions
            )
        }
    }

    # 6. Attach milestone if reached
    if streak_result["milestone"]:
        m_data = streak_result["milestone"]
        if m_data.get("show_donation"):
            from app.donations.service import create_donation_prompt
            prompt = create_donation_prompt(
                db=db,
                user_id=user_id,
                milestone=m_data["milestone"]
            )
            m_data["prompt_id"] = str(prompt.id)

        response["milestone"] = m_data

    logger.info(
        "completion_pipeline_finished",
        extra={
            "user_id": str(user_id),
            "session_id": str(session_id),
            "streak": (
                streak_result["streak"]
                .current_streak
            ),
            "milestone": (
                streak_result["milestone"]
                ["milestone"]
                if streak_result["milestone"]
                else None
            )
        }
    )

    return response


def _get_pre_strain_score(db, session):
    """
    Retrieves the strain score that
    triggered this session, if available.
    """

    if not session.strain_log_id:
        return 0

    from app.strain_engine.models import (
        StrainLog
    )

    strain = db.query(
        StrainLog
    ).filter(
        StrainLog.id
        == session.strain_log_id
    ).first()

    if strain:
        return strain.strain_score

    return 0
