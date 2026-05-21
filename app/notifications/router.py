from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.strain_engine.models import (
    StrainLog
)

from app.notifications.service import (
    process_notification
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.post(
    "/process/{strain_id}"
)
def trigger_notification(
    strain_id: str,
    db: Session = Depends(get_db)
):

    strain_log = db.query(
        StrainLog
    ).filter(
        StrainLog.id == strain_id
    ).first()

    if not strain_log:
        raise HTTPException(
            status_code=404,
            detail="Strain log not found"
        )

    notification = process_notification(
        db=db,
        strain_log=strain_log
    )

    if not notification:
        return {
            "message":
            "No notification triggered"
        }

    return notification