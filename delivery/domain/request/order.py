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

class OrderReq(BaseModel):
    total: Optional[float] = None
    observation: Optional[str] = None
    address_id: Optional[UUID] = None
    store_id: Optional[UUID] = None
    status: Optional[StatusChoices] = None
    products: Optional[List[UUID]] = None
    payment_method: Optional[str] = None
    
    class Config:
        from_attributes = True