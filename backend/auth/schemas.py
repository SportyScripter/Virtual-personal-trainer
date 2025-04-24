from pydantic import BaseModel, EmailStr
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
