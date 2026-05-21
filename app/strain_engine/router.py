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

from app.context_engine.models import (
    ContextLog
)

from app.strain_engine.service import (
    generate_strain_state
)

router = APIRouter(
    prefix="/strain",
    tags=["Strain"]
)


@router.post(
    "/calculate/{telemetry_id}"
)
def calculate_strain(
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

    contexts = db.query(
        ContextLog
    ).filter(
        ContextLog.telemetry_id
        == telemetry.id
    ).all()

    strain = generate_strain_state(
        db=db,
        telemetry=telemetry,
        contexts=contexts
    )

    return strain