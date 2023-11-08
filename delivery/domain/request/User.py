from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List
from .Address import AddressReq
from .Rating import RatingReq
from .Order import OrderReq
class UserReq(BaseModel):
    name: str
    birthdate: date
    document: str
    phone: Optional[str]
    email: str
    password: str
    whatsapp: Optional[str]
    instagram: Optional[str]
    role: str
    class Config:
        orm_mode = True
