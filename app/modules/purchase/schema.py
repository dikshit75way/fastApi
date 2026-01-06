from pydantic import BaseModel 
from datetime import datetime
from typing import Optional

class PurchaseCreate(BaseModel):
    buyer_id : int 
    project_id : int 
    payment_method: str = "wallet" # wallet or stripe

class PurchaseOut(BaseModel):
    id : int 
    buyer_id : int 
    project_id : int 
    amount : int 
    status : str 
    commission : int 
    created_at : datetime
    checkout_url: Optional[str] = None

    class Config:
        from_attributes = True