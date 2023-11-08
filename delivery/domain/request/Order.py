from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List, Any
from .product import ProductReq
    
class OrderReq(BaseModel):
    total: float
    observation: Optional[str]
    address_id: UUID
    store_id: UUID
    products: List[ProductReq]
    
    class Config:
        orm_mode = True