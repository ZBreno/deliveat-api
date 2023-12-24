from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List, Any
from .product import ProductBonusAssociationReq
    
class OrderReq(BaseModel):
    total: float
    observation: Optional[str] = None
    # address_id: UUID
    # store_id: UUID
    products: Optional[List[ProductBonusAssociationReq]]
    payment_method: str
    
    class Config:
        from_attributes = True