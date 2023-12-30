from pydantic import BaseModel
    
class NotificationReq(BaseModel):
    text: str
    phone: str
    
    class Config:
        from_attributes = True
    
    
    