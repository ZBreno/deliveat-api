from pydantic import BaseModel
from typing import Optional


class ProductBonusReq(BaseModel):
    name: str
    description: Optional[str] = None
    cost: float    
    
    class Config:
        orm_mode = True