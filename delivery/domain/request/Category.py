from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List, Any


class CategoryReq(BaseModel):
    
    id: Optional[UUID]
    name: str
    
    
    # @validator('id', pre=True, allow_reuse=True, check_fields=False)
    # def category_object_to_uuid(cls, values):
    #     if isinstance(values, UUID):
    #         return values
    #     else:
    #         return values.id.id
        
    class Config:
        orm_mode = True