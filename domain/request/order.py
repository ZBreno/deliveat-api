from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List, Any
from .product import ProductReq
    
class OrderReq(BaseModel):
    total: float
    observation: Optional[str] = None
    address_id: UUID
    store_id: UUID
    products: UUID
    
    class Config:
        from_attributes = True