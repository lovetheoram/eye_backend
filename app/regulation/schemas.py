from pydantic import (
    BaseModel,
    Field
)

from app.regulation.enums import (
    RegulationMode
)


class RegulationSessionCreate(
    BaseModel
):

    mode: RegulationMode

    duration_seconds: int = Field(
        ge=30,
        le=1800
    )

    strain_log_id: str | None = None


class RegulationSessionResponse(
    BaseModel
):

    id: str

    mode: str

    duration_seconds: int

    completed: bool

    class Config:
        from_attributes = True