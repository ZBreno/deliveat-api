from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List
from .address import AddressReq
from .rating import RatingReq
from .order import OrderReq
class UserReq(BaseModel):
    name: str
    birthdate: date
    document: str
    phone: Optional[str] = None
    email: str
    password: str
    whatsapp: Optional[str] = None
    instagram: Optional[str] = None
    role: str
    class Config:
        orm_mode = True
