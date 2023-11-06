from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List, Any
from .product import ProductReq
    
class OrderReq(BaseModel):
    id: Optional[UUID]
    total: float
    observation: Optional[str]
    address_id: UUID
    store_id: UUID
    user_id: UUID
    products: List[ProductReq]
    products_bonus: List[ProductReq]
    
    
    @validator('id', pre=True, allow_reuse=True, check_fields=False)
    def order_object_to_uuid(cls, values):
        if isinstance(values, UUID):
            return values
        else:
            return values.id.id
        
    @validator('address_id', pre=True, allow_reuse=True, check_fields=False)
    def address_object_to_uuid(cls, values):
        if isinstance(values, UUID):
            return values
        else:
            return values.id.id
        
    @validator('store_id', pre=True, allow_reuse=True, check_fields=False)
    def store_object_to_uuid(cls, values):
        if isinstance(values, UUID):
            return values
        else:
            return values.id.id
        
    @validator('user_id', pre=True, allow_reuse=True, check_fields=False)
    def user_object_to_uuid(cls, values):
        if isinstance(values, UUID):
            return values
        else:
            return values.id.id
        
    @validator('id', pre=True, allow_reuse=True, check_fields=False)
    def order_object_to_uuid(cls, values):
        if isinstance(values, UUID):
            return values
        else:
            return values.id.id
    
    @validator('products_bonus', pre=True, allow_reuse=True, check_fields=False)
    def products_set_to_list(cls, values):
        return [v.to_dict() for v in values]
    
    @validator('products', pre=True, allow_reuse=True, check_fields=False)
    def products_bonus_set_to_list(cls, values):
        return [v.to_dict() for v in values]
    
    class Config:
        orm_mode = True