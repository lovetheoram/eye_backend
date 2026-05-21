from pydantic import BaseModel


class NotificationResponse(BaseModel):

    notification_type: str

    message: str

    delivered: bool

    class Config:
        from_attributes = True