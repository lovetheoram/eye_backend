from pydantic import BaseModel


class StrainResponse(BaseModel):

    strain_score: int

    risk_level: str

    recovery_needed: bool

    recovery_debt: int

    class Config:
        from_attributes = True