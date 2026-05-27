from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.telemetry.models import (
    TelemetryLog
)

from app.context_engine.service import (
    generate_contexts
)

router = APIRouter(
    prefix="/contexts",
    tags=["Contexts"]
)


@router.post(
    "/generate/{telemetry_id}"
)
def generate_behavioral_contexts(
    telemetry_id: str,
    db: Session = Depends(get_db)
):

    telemetry = db.query(
        TelemetryLog
    ).filter(
        TelemetryLog.id == telemetry_id
    ).first()

    if not telemetry:
        raise HTTPException(
            status_code=404,
            detail="Telemetry not found"
        )

    contexts = generate_contexts(
        db=db,
        telemetry=telemetry
    )

    return {
        "contexts": [
            c.context_name
            for c in contexts
        ]
    }