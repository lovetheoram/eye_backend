from pydantic import BaseModel


class ContextResponse(BaseModel):

    context_name: str

    class Config:
        from_attributes = True