from pydantic import BaseModel

from typing import Optional


class StreakResponse(BaseModel):

    current_streak: int

    longest_streak: int

    total_completions: int

    last_completion_at: Optional[str] = None

    class Config:
        from_attributes = True


class MilestoneResponse(BaseModel):

    milestone: int

    message: str

    show_donation: bool
