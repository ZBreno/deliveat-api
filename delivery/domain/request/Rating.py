from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List, Any

class RatingReq(BaseModel):
    
    rating: float
    description: Optional[str]
    user_id: UUID
    order_id: UUID
    
    class Config:
        orm_mode = True