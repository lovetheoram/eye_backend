from pydantic import BaseModel


class InsightResponse(
    BaseModel
):

    title: str

    message: str

    insight_type: str

    class Config:
        from_attributes = True