from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List, Any


class CategoryReq(BaseModel):
    
    name: str
        
    class Config:
        from_attributes = True