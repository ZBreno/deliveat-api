from pydantic import BaseModel
from datetime import date
from typing import Optional
from fastapi import UploadFile

class UserReq(BaseModel):
    name: str
    birthdate: Optional[date] = None
    document: Optional[str] = None
    phone: Optional[str] = None
    email: str
    password: str
    whatsapp: Optional[str] = None
    instagram: Optional[str] = None
    profile_picture: Optional[UploadFile] = None
    role: str
    class Config:
        from_attributes = True

class UpdateUserReq(BaseModel):
    name: Optional[str] = None
    birthdate: Optional[date] = None
    document: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    instagram: Optional[str] = None

    class Config:
        from_attributes = True

class LoginReq(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True