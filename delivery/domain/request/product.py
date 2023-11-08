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
    categories: Optional[List[CategoryReq]] = []
    products_bonus: Optional[List[ProductBonusReq]] = []
    
    class Config:
        orm_mode = True