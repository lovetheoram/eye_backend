from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.auth.dependencies import (
    get_current_user
)

from app.focal_isolation.models import (
    FocalIsolationSession
)

from app.focal_isolation.schemas import (
    FocalIsolationStart,
    FocalIsolationComplete,
    FocalIsolationSkip
)

from app.focal_isolation.service import (
    create_session,
    complete_session,
    skip_session
)

router = APIRouter(
    prefix="/focal-isolation",
    tags=["Focal Isolation"]
)


@router.post("/start")
def start_focal_isolation(
    payload: FocalIsolationStart,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):
    """
    Start a new 20-second focal isolation
    session. Returns the dot pattern config
    for the client to render.
    """

    result = create_session(
        db=db,
        user_id=current_user.id,
        payload=payload
    )

    return result["config"]


@router.patch(
    "/complete/{session_id}"
)
def complete_focal_isolation(
    session_id: str,
    payload: FocalIsolationComplete,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):
    """
    Complete a focal isolation session.
    Server validates integrity — rejects
    fake or too-fast completions.
    """

    from app.orchestration.completion_pipeline import process_session_completion

    result = process_session_completion(
        db=db,
        user_id=current_user.id,
        session_id=session_id,
        client_report=payload
    )

    if not result["success"]:
        if result.get("error") == "session_not_found":
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )
        raise HTTPException(
            status_code=422,
            detail=result.get("error")
        )

    return result


@router.patch(
    "/skip/{session_id}"
)
def skip_focal_isolation(
    session_id: str,
    payload: FocalIsolationSkip = None,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):
    """
    Mark a session as skipped.
    Tracked for behavioral analysis.
    """

    session = db.query(
        FocalIsolationSession
    ).filter(
        FocalIsolationSession.id
        == session_id,
        FocalIsolationSession.user_id
        == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    skip_session(
        db=db,
        session=session
    )

    return {
        "status": "skipped",
        "message": (
            "Session skipped. "
            "We'll remind you again soon."
        )
    }


@router.get("/active")
def get_active_session(
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):
    """
    Check if the user has an active
    (not yet completed/skipped) session.
    """

    session = db.query(
        FocalIsolationSession
    ).filter(
        FocalIsolationSession.user_id
        == current_user.id,
        FocalIsolationSession.status
        == "active"
    ).order_by(
        FocalIsolationSession.created_at
        .desc()
    ).first()

    if not session:
        return {"active": False}

    return {
        "active": True,
        "session_id": str(session.id),
        "pattern_type": session.pattern_type,
        "duration_ms": session.duration_ms
    }
