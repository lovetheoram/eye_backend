from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.auth.dependencies import (
    get_current_user
)

from app.recovery_engine.schemas import (
    RecoveryCreate
)

from app.recovery_engine.service import (
    create_recovery_log
)

router = APIRouter(
    prefix="/recovery",
    tags=["Recovery"]
)


@router.post("/log")
def log_recovery(

    payload: RecoveryCreate,

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )
):

    recovery = create_recovery_log(

        db=db,

        user_id=current_user.id,

        payload=payload
    )

    return recovery