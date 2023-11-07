from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List, Any

class RatingReq(BaseModel):
    
    id: Optional[UUID]
    rating: float
    description: Optional[str]
    user_id: UUID
    order_id: UUID
    
    
    # @validator('id', pre=True, allow_reuse=True, check_fields=False)
    # def rating_object_to_uuid(cls, values):
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
        
    @validator('order_id', pre=True, allow_reuse=True, check_fields=False)
    def order_object_to_uuid(cls, values):
        if isinstance(values, UUID):
            return values
        else:
            return values.id.id
    
    class Config:
        orm_mode = True