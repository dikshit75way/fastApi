from pydantic import BaseModel
from datetime import datetime


class PurchaseBase(BaseModel):
    price: int 

class PurchaseOut(PurchaseBase):
    id: int 
    created_at: datetime

    class Config:
        from_attributes = True