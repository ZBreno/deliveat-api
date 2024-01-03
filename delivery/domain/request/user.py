from pydantic import BaseModel
from datetime import date
from typing import Optional
from fastapi import UploadFile, File, Form
from domain.data.enums.role import RoleChoice

class UserReq(BaseModel):
    name: str
    birthdate: Optional[date] = None
    document: Optional[str] = None
    phone: Optional[str] = None
    email: str
    password: str
    instagram: Optional[str] = None
    profile_picture: Optional[str] = None
    delivery_cost: Optional[float] = None
    time_prepare: Optional[str] = None
    role: RoleChoice
    class Config:
        from_attributes = True

class UpdateUserReq(BaseModel):
    name: Optional[str] = Form(None),
    birthdate: Optional[date] = Form(None),
    document: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    instagram: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    profile_picture: UploadFile = File(None)
    delivery_cost: Optional[float] = Form(None)
    time_prepare: Optional[str] = Form(None)

    class Config:
        from_attributes = True

class LoginReq(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True