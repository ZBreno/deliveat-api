from pydantic import BaseModel, validator
from uuid import UUID
from typing import Optional

class AddressReq(BaseModel):
    street: str
    city: str
    district: str
    number: str
    complement: Optional[str]
    reference_point: Optional[str]
    
    class Config:
        orm_mode = True
        