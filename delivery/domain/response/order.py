from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List
from domain.request.product import ProductReq
from domain.data.enums.status_order import StatusChoices

class OrderResponse(BaseModel):
    id: UUID
    total: float
    observation: Optional[str] = None
    address_id: UUID
    store_id: UUID
    status: StatusChoices
    products: Optional[List[ProductReq]]
    user_id: UUID
    payment_method: str
    
    class Config:
        from_attributes = True