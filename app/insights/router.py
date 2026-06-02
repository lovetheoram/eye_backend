from datetime import datetime, timezone, timedelta

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

from app.focal_isolation.models import FocalIsolationSession
from app.regulation.models import RegulationSession

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


@router.get("/weekly-report")
def get_weekly_report(
    tz_offset: int = 0,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get the Focus Stamina Report for the weekly summary.
    """
    now_utc = datetime.now(timezone.utc)
    seven_days_ago = now_utc - timedelta(days=7)

    # 1. Recovery sessions
    completed_focal = db.query(FocalIsolationSession).filter(
        FocalIsolationSession.user_id == current_user.id,
        FocalIsolationSession.completed == True,
        FocalIsolationSession.created_at >= seven_days_ago
    ).count()

    completed_reg = db.query(RegulationSession).filter(
        RegulationSession.user_id == current_user.id,
        RegulationSession.completed == True,
        RegulationSession.created_at >= seven_days_ago
    ).count()

    recovery_sessions = completed_focal + completed_reg

    # 2. Average strain & best/worst days
    strain_logs = db.query(StrainLog).filter(
        StrainLog.user_id == current_user.id,
        StrainLog.created_at >= seven_days_ago
    ).all()

    average_strain = 0.0
    best_day = "None"
    worst_day = "None"

    if strain_logs:
        average_strain = round(sum(log.strain_score for log in strain_logs) / len(strain_logs), 1)

        # Group by weekday in local time
        weekday_scores = {}
        for log in strain_logs:
            local_time = log.created_at - timedelta(minutes=tz_offset)
            weekday_name = local_time.strftime("%A")
            if weekday_name not in weekday_scores:
                weekday_scores[weekday_name] = []
            weekday_scores[weekday_name].append(log.strain_score)

        weekday_averages = {day: sum(scores)/len(scores) for day, scores in weekday_scores.items()}

        if weekday_averages:
            best_day = min(weekday_averages, key=weekday_averages.get)
            worst_day = max(weekday_averages, key=weekday_averages.get)

    # 3. Current streak
    from app.streaks.service import get_user_streak
    user_streak = get_user_streak(db=db, user_id=current_user.id)
    streak = user_streak.current_streak if user_streak else 0

    return {
        "recovery_sessions": recovery_sessions,
        "average_strain": average_strain,
        "best_day": best_day,
        "worst_day": worst_day,
        "streak": streak
    }


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