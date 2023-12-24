from pydantic import BaseModel, validator
from uuid import UUID
from typing import Optional

class AddressReq(BaseModel):
    street: str
    city: str
    district: str
    number: Optional[str] = None
    complement: Optional[str] = None
    reference_point: Optional[str] = None
    
    class Config:
        from_attributes = True
        