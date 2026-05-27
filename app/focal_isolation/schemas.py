from pydantic import (
    BaseModel,
    Field
)

from typing import Optional


class FocalIsolationStart(BaseModel):

    strain_log_id: Optional[str] = None

    notification_id: Optional[str] = None

    pattern_type: str = "linear"


class FocalIsolationComplete(BaseModel):

    client_frame_count: int = Field(
        ge=0,
        description=(
            "Number of animation frames "
            "the client actually rendered."
        )
    )


class FocalIsolationSkip(BaseModel):

    reason: Optional[str] = None


class FocalIsolationConfigResponse(
    BaseModel
):

    session_id: str

    pattern: dict

    dot_color: str

    duration_ms: int

    expected_frame_count: int

    class Config:
        from_attributes = True


class FocalIsolationResponse(BaseModel):

    id: str

    status: str

    completed: bool

    skipped: bool

    integrity_score: Optional[float] = None

    pattern_type: str

    duration_ms: int

    class Config:
        from_attributes = True
