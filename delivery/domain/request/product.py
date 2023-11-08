from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List, Any
from .Category import CategoryReq

class ProductReq(BaseModel):
    name: str
    description: Optional[str]
    cost: float
    categories: List[CategoryReq]
    product_bonus: Optional[List[UUID]]
    
    # @validator('categories', pre=True, allow_reuse=True)
    # def categories_set_to_list(cls, categories):
    #     print(categories)
    #     return [c.to_dict() for c in categories]
    
    class Config:
        orm_mode = True