from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

from app.support.helper import format_datetime


# Shared properties
class UserBase(BaseModel):
    id: int
    username: str
    nickname: str
    gender: str
    avatar: str

    class Config:
        orm_mode = True


class UserDetail(UserBase):
    name: Optional[str] = None
    id_number: Optional[datetime] = None
    birth: Optional[str] = None
    cellphone: Optional[str] = None
    email: Optional[str] = None
    email_verified_at: Optional[datetime] = None
    state: str
    identity: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    cellphone: Optional[str] = None
    email: Optional[str] = None
    id_number: Optional[datetime] = None
    birth: Optional[str] = None
    state: str
    identity: str