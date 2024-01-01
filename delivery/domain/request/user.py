from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List
from domain.data.enums.role import RoleChoice

class UserReq(BaseModel):
    name: str
    birthdate: Optional[date] = None
    document: Optional[str] = None
    phone: Optional[str] = None
    email: str
    password: str
    whatsapp: Optional[str] = None
    instagram: Optional[str] = None
    role: RoleChoice
    class Config:
        from_attributes = True

class LoginReq(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True