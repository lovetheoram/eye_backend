from pydantic import BaseModel

from typing import Optional


class DonationAction(BaseModel):

    action_taken: str


class DonationConfigResponse(BaseModel):

    payment_app: str

    display_name: str

    deep_link_template: str

    upi_id: Optional[str] = None

    suggested_amounts: str

    icon_name: Optional[str] = None

    class Config:
        from_attributes = True


class DonationPromptResponse(BaseModel):

    id: str

    streak_milestone: int

    message: str

    payment_options: list[
        DonationConfigResponse
    ]

    class Config:
        from_attributes = True
