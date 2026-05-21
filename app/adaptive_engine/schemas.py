from pydantic import BaseModel


class BehavioralProfileResponse(
    BaseModel
):

    focus_profile: str

    recovery_profile: str

    avg_focus_duration: int

    adaptive_strain_threshold: int

    class Config:
        from_attributes = True