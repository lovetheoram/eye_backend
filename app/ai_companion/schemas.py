from pydantic import BaseModel


class ConversationRequest(
    BaseModel
):

    message: str


class ConversationResponse(
    BaseModel
):

    assistant_response: str

    emotional_tone: str

    class Config:
        from_attributes = True