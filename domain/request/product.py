from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List, Any, Dict
from .category import CategoryAssociationReq
from .product_bonus import ProductBonusReq
from domain.data.sqlalchemy_models import Category
class ProductReq(BaseModel):
    name: str
    description: Optional[str] = None
    cost: float
    categories: Optional[List[CategoryAssociationReq]]
    products_bonus: Optional[List[UUID]] = []
    
    class Config:
        from_attributes = True
    