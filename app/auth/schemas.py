from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    name: str

    email: EmailStr

    password: str = Field(
        ...,
        min_length=4,
        max_length=64
    )

    work_type: str | None = None


class UserLogin(BaseModel):
    email: EmailStr

    password: str = Field(
        ...,
        min_length=4,
        max_length=64
    )
    expo_push_token: str | None = None

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    work_type: str | None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str