from pydantic import BaseModel, EmailStr, Field
import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    user_role: str


class RequestDetails(BaseModel):
    email: str
    password: str


class TokenSchama(BaseModel):
    access_token: str
    refresh_token: str


class ChangePassword(BaseModel):
    email: str
    old_password: str
    new_password: str


class TokenCreate(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
    status: bool
    created_at: datetime.datetime


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    profile_image: str | None = None
    create_at: datetime.datetime
    updated_at: datetime.datetime | None = None

    class Config:
        orm_mode = True

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8, description="Password must be at least 8 characters long")
    confirm_password: str
    
    
