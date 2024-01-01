from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List
from domain.data.enums.status_order import StatusChoices

class OrderReq(BaseModel):
    total: float
    observation: Optional[str] = None
    address_id: UUID
    store_id: UUID
    status: StatusChoices
    products: Optional[List[UUID]]
    payment_method: str
    
    class Config:
        from_attributes = True