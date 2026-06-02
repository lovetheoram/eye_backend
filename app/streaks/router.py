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

from app.streaks.service import (
    get_user_streak
)

from app.streaks.milestones import (
    MILESTONES
)

from app.focal_isolation.models import FocalIsolationSession
from app.regulation.models import RegulationSession

router = APIRouter(
    prefix="/streaks",
    tags=["Streaks"]
)


@router.get("/me")
def get_my_streak(
    tz_offset: int = 0,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):
    """
    Get the current user's streak data, today's completed resets,
    and rolling 7-day recovery success rate.
    """

    streak = get_user_streak(
        db=db,
        user_id=current_user.id
    )

    # Compute Today's Resets in user's local timezone
    now_utc = datetime.now(timezone.utc)
    local_now = now_utc - timedelta(minutes=tz_offset)
    local_today_start = datetime(local_now.year, local_now.month, local_now.day)
    utc_today_start = local_today_start + timedelta(minutes=tz_offset)
    utc_today_start = utc_today_start.replace(tzinfo=timezone.utc)

    today_focal = db.query(FocalIsolationSession).filter(
        FocalIsolationSession.user_id == current_user.id,
        FocalIsolationSession.completed == True,
        FocalIsolationSession.completed_at >= utc_today_start
    ).count()

    today_reg = db.query(RegulationSession).filter(
        RegulationSession.user_id == current_user.id,
        RegulationSession.completed == True,
        RegulationSession.created_at >= utc_today_start
    ).count()

    today_resets = today_focal + today_reg

    # Compute Weekly Recovery Rate (rolling 7 days)
    seven_days_ago = now_utc - timedelta(days=7)

    completed_focal_week = db.query(FocalIsolationSession).filter(
        FocalIsolationSession.user_id == current_user.id,
        FocalIsolationSession.completed == True,
        FocalIsolationSession.created_at >= seven_days_ago
    ).count()

    skipped_focal_week = db.query(FocalIsolationSession).filter(
        FocalIsolationSession.user_id == current_user.id,
        FocalIsolationSession.skipped == True,
        FocalIsolationSession.created_at >= seven_days_ago
    ).count()

    completed_reg_week = db.query(RegulationSession).filter(
        RegulationSession.user_id == current_user.id,
        RegulationSession.completed == True,
        RegulationSession.created_at >= seven_days_ago
    ).count()

    total_completed = completed_focal_week + completed_reg_week
    total_initiated = total_completed + skipped_focal_week

    if total_initiated > 0:
        weekly_recovery_rate = int(round((total_completed / total_initiated) * 100))
    else:
        weekly_recovery_rate = 100  # default to 100% if no sessions

    return {
        "current_streak": (
            streak.current_streak
        ),
        "longest_streak": (
            streak.longest_streak
        ),
        "total_completions": (
            streak.total_completions
        ),
        "last_completion_at": (
            str(streak.last_completion_at)
            if streak.last_completion_at
            else None
        ),
        "today_resets": today_resets,
        "weekly_recovery_rate": weekly_recovery_rate
    }


@router.get("/me/milestones")
def get_upcoming_milestones(
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):
    """
    Get upcoming milestones relative to
    the user's current streak.
    """

    streak = get_user_streak(
        db=db,
        user_id=current_user.id
    )

    current = streak.current_streak

    upcoming = [
        {
            "milestone": m,
            "remaining": m - current
        }
        for m in MILESTONES
        if m > current
    ]

    return {
        "current_streak": current,
        "upcoming_milestones": upcoming
    }
