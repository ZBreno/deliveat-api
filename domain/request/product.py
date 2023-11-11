from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List, Any, Dict
from .category import CategoryReq
from .product_bonus import ProductBonusReq
class ProductReq(BaseModel):
    name: str
    description: Optional[str] = None
    cost: float
    categories: Optional[List[UUID]] = []
    products_bonus: Optional[List[UUID]] = []
    
    class Config:
        from_attributes = True
    
