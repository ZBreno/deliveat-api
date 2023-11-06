from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List, Any
from .category import CategoryReq

class ProductReq(BaseModel):
    id: Optional[UUID]
    name: str
    description: str
    cost: float
    categories: List[CategoryReq]
    
    @validator('id', pre=True, allow_reuse=True, check_fields=False)
    def product_object_to_uuid(cls, values):
        if isinstance(values, UUID):
            return values
        else:
            return values.id.id
        
    @validator('categories', pre=True, allow_reuse=True, check_fields=False)
    def categories_set_to_list(cls, values):
        return [v.to_dict() for v in values]
    
    class Config:
        orm_mode = True