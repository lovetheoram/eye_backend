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

from app.regulation.models import (
    RegulationSession
)

from app.regulation.schemas import (
    RegulationSessionCreate
)

from app.regulation.service import (
    create_regulation_session,
    complete_regulation_session
)

router = APIRouter(
    prefix="/regulation",
    tags=["Regulation"]
)


@router.post("/start")
def start_regulation_session(
    payload: RegulationSessionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):

    session = (
        create_regulation_session(
            db=db,
            user_id=current_user.id,
            payload=payload
        )
    )

    return session


@router.patch(
    "/complete/{session_id}"
)
def complete_session(
    session_id: str,
    db: Session = Depends(get_db)
):

    session = db.query(
        RegulationSession
    ).filter(
        RegulationSession.id
        == session_id
    ).first()

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    session = complete_regulation_session(
        db=db,
        session=session
    )

    return session