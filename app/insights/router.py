from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.auth.dependencies import (
    get_current_user
)

from app.insights.models import (
    InsightLog
)

from app.strain_engine.models import (
    StrainLog
)

from app.recovery_engine.models import (
    RecoveryLog
)

from app.insights.service import (
    generate_user_insights
)

from app.insights.schemas import (
    InsightResponse
)

router = APIRouter(
    prefix="/insights",
    tags=["Insights"]
)


@router.post(
    "/generate",
    response_model=list[
        InsightResponse
    ]
)
def generate_insights(

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )
):

    strain_logs = db.query(
        StrainLog
    ).filter(
        StrainLog.user_id
        == current_user.id
    ).all()

    recovery_logs = db.query(
        RecoveryLog
    ).filter(
        RecoveryLog.user_id
        == current_user.id
    ).all()

    insights = generate_user_insights(
        db=db,
        user_id=current_user.id,
        strain_logs=strain_logs,
        recovery_logs=recovery_logs
    )

    return insights


@router.get(
    "/latest",
    response_model=InsightResponse | None
)
def get_latest_insight(

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )
):

    insight = db.query(
        InsightLog
    ).filter(
        InsightLog.user_id
        == current_user.id
    ).order_by(
        InsightLog.created_at.desc()
    ).first()

    return insight


@router.get(
    "/history",
    response_model=list[
        InsightResponse
    ]
)
def get_insight_history(

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    )
):

    insights = db.query(
        InsightLog
    ).filter(
        InsightLog.user_id
        == current_user.id
    ).order_by(
        InsightLog.created_at.desc()
    ).all()

    return insights