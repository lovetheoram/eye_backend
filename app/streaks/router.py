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

router = APIRouter(
    prefix="/streaks",
    tags=["Streaks"]
)


@router.get("/me")
def get_my_streak(
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    )
):
    """
    Get the current user's streak data.
    """

    streak = get_user_streak(
        db=db,
        user_id=current_user.id
    )

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
        )
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
