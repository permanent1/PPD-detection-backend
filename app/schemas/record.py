from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserDetail

# Shared properties
class RecordBase(BaseModel):
    id: int
    result: str

    class Config:
        orm_mode = True


class RecordDetail(RecordBase):
    user_id: int
    result: Optional[str] = None
    image: Optional[str] = None
    res_image: Optional[str] = None
    size: Optional[float] = None
    length: Optional[float] = None
    width: Optional[float] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RecordDetail_m(RecordBase):
    user_id: UserDetail
    result: Optional[str] = None
    image: Optional[str] = None
    res_image: Optional[str] = None
    size: Optional[float] = None
    length: Optional[float] = None
    width: Optional[float] = None
    description: Optional[str] = None


class RecordCreate(BaseModel):
    user_id: int
    result: Optional[str] = None
    image: Optional[str] = None
    res_image: Optional[str] = None
    size: Optional[float] = None
    length: Optional[float] = None
    width: Optional[float] = None
    description: Optional[str] = None


class RecordUpdate(BaseModel):
    result: Optional[str] = None
    image: Optional[str] = None
    res_image: Optional[str] = None
    size: Optional[float] = None
    length: Optional[float] = None
    width: Optional[float] = None
    description: Optional[str] = None
