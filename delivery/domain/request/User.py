from pydantic import BaseModel, validator
from uuid import UUID
from datetime import date
from typing import Optional, List
from .address import AddressReq
from .rating import RatingReq
from .order import OrderReq
class UserReq(BaseModel):
    id: Optional[UUID]
    name: str
    birthdate: date
    document: str
    phone: Optional[str]
    email: str
    password: str
    whatsapp: Optional[str]
    instagram: Optional[str]
    role: str
    
    addresses: List[AddressReq]
    orders: List[OrderReq]
    orders_store: List[OrderReq]
    ratings: List[RatingReq]

    # @validator('id', pre=True, allow_reuse=True, check_fields=False)
    # def user_object_to_uuid(cls, values):
    #     if isinstance(values, UUID):
    #         return values
    #     else:
    #         return values.id.id

    @validator('addresses', pre=True, allow_reuse=True, check_fields=False)
    def addresses_set_to_list(cls, values):
        return [v.to_dict() for v in values]

    @validator('orders', pre=True, allow_reuse=True, check_fields=False)
    def orders_set_to_list(cls, values):
        return [v.to_dict() for v in values]

    @validator('orders_store', pre=True, allow_reuse=True, check_fields=False)
    def orders_store_set_to_list(cls, values):
        return [v.to_dict() for v in values]

    @validator('ratings', pre=True, allow_reuse=True, check_fields=False)
    def ratings_set_to_list(cls, values):
        return [v.to_dict() for v in values]

    class Config:
        orm_mode = True
