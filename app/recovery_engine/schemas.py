from pydantic import BaseModel


from typing import Optional

class RecoveryCreate(
    BaseModel
):

    regulation_session_id: Optional[str] = None

    focal_isolation_session_id: Optional[str] = None

    feedback: str


class RecoveryResponse(
    BaseModel
):

    recovery_delta: int

    recovery_status: str

    class Config:
        from_attributes = True