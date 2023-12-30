from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class ProductBonusReq(BaseModel):
    name: str
    description: Optional[str] = None
    cost: float    
    
    class Config:
        from_attributes = True
class ProductBonusAssociationReq(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    cost: float
    
    class Config:
        from_attributes = True