from sqlalchemy.orm import Session

from app.strain_engine.models import (
    StrainLog
)

from app.strain_engine.scoring import (
    calculate_strain_score
)

from app.strain_engine.risk import (
    classify_risk
)


def generate_strain_state(
    db: Session,
    telemetry,
    contexts
):

    score = calculate_strain_score(
        telemetry,
        contexts
    )

    risk = classify_risk(score)

    recovery_needed = score >= 7

    recovery_debt = max(score - 5, 0)

    strain_log = StrainLog(

        user_id=telemetry.user_id,

        telemetry_id=telemetry.id,

        strain_score=score,

        risk_level=risk.value,

        recovery_needed=recovery_needed,

        recovery_debt=recovery_debt
    )

    db.add(strain_log)

    db.commit()

    db.refresh(strain_log)

    return strain_log