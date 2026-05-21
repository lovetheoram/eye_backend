from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.auth.dependencies import (
    get_current_user
)

from app.telemetry.models import (
    TelemetryLog
)

from app.recovery_engine.models import (
    RecoveryLog
)

from app.adaptive_engine.service import (
    build_behavioral_profile
)

router = APIRouter(
    prefix="/adaptive",
    tags=["Adaptive Engine"]
)


@router.post("/profile")
def generate_behavioral_profile(
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):

    telemetry_logs = db.query(
        TelemetryLog
    ).filter(
        TelemetryLog.user_id
        == current_user.id
    ).all()

    recovery_logs = db.query(
        RecoveryLog
    ).filter(
        RecoveryLog.user_id
        == current_user.id
    ).all()

    profile = build_behavioral_profile(
        db=db,
        user_id=current_user.id,
        telemetry_logs=telemetry_logs,
        recovery_logs=recovery_logs
    )

    return profile