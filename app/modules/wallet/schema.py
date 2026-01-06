from pydantic import BaseModel
from datetime import datetime

class WalletCreate(BaseModel):
    user_id : int 
    type : str 
    reference_id : int 
    source : str 
    amount : int 

class WalletOut(BaseModel):
    id : int 
    user_id : int 
    type : str 
    reference_id : int 
    source : str 
    amount : int 
    created_at : datetime

    class Config:
        from_attributes = True


class Widhdraw(BaseModel):
    user_id : int 
    amount : int


class WidhdrawOut(BaseModel):
    id : int 
    user_id : int 
    amount : int 
    created_at : datetime

    class Config:
        from_attributes = True


class WalletAdd(BaseModel):
    user_id : int 
    amount : int