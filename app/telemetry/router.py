from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

# from app.core.database import get_db
from app.db.session import get_db

from app.auth.dependencies import (
    get_current_user
)

from app.telemetry.schemas import (
    TelemetryHeartbeatCreate,
    TelemetryResponse
)

from app.telemetry.service import (
    create_telemetry_log
)

from app.orchestration.behavioral_pipeline import process_behavioral_heartbeat
router = APIRouter(
    prefix="/telemetry",
    tags=["Telemetry"]
)


@router.post(
    "/heartbeat",
    response_model=TelemetryResponse
)
def heartbeat(
    payload: TelemetryHeartbeatCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    telemetry = create_telemetry_log(
        db=db,
        user_id=current_user.id,
        payload=payload
    )

    return telemetry

@router.post("/heartbeat_notification")
def heartbeat_notification(
    payload: TelemetryHeartbeatCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):

    result = process_behavioral_heartbeat(
        db=db,
        user_id=current_user.id,
        payload=payload
    )

    return result