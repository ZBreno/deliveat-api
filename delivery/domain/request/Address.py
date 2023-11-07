from pydantic import BaseModel, validator
from uuid import UUID
from typing import Optional

class AddressReq(BaseModel):
    street: str
    city: str
    district: int
    number: str
    complement: Optional[str]
    reference_point: Optional[str]
    
    class Config:
        orm_mode = True
    
    # @validator('id', pre=True, allow_reuse=True, check_fields=False)
    # def address_object_to_uuid(cls, values):
    #     if isinstance(values, UUID):
    #         return values
    #     else:
    #         return values.id.id
    
    @validator('user_id', pre=True, allow_reuse=True, check_fields=False)
    def user_object_to_uuid(cls, values):
        if isinstance(values, UUID):
            return values
        else:
            return values.id.id
        