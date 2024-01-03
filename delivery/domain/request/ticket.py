from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional
    
class TicketReq(BaseModel):
    deadline: date
    code: str
    description: Optional[str] = None
    discount: float
    title: str
    
    class Config:
        from_attributes = True
    