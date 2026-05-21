from pydantic import BaseModel, Field
from uuid import UUID

from app.telemetry.enums import (
    TimeOfDay
)


class TelemetryHeartbeatCreate(BaseModel):

    app_name: str

    screen_on_minutes: int = Field(
        ge=0,
        le=1440
    )

    continuous_focus_minutes: int = Field(
        ge=0,
        le=1440
    )

    brightness_level: int = Field(
        ge=0,
        le=100
    )

    session_count: int = Field(
        ge=0
    )

    time_of_day: TimeOfDay


class TelemetryResponse(BaseModel):

    id: UUID

    app_name: str

    app_category: str

    screen_on_minutes: int

    continuous_focus_minutes: int

    brightness_level: int

    session_count: int

    time_of_day: str

    class Config:
        from_attributes = True