from pydantic import BaseModel, EmailStr, constr
from uuid import UUID


class SignupRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=32)
    name: constr(min_length=2, max_length=20)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
