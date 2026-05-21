from pydantic import BaseModel


class RecoveryCreate(
    BaseModel
):

    regulation_session_id: str

    feedback: str


class RecoveryResponse(
    BaseModel
):

    recovery_delta: int

    recovery_status: str

    class Config:
        from_attributes = True