from pydantic import BaseModel 
from datetime import datetime

class ReviewCreate(BaseModel):
    user_id : int 
    project_id : int 
    rating : int 
    comment : str 

class ReviewOut(BaseModel):
    id : int 
    user_id : int 
    project_id : int 
    rating : int 
    comment : str 
    created_at : datetime

    class Config:
        from_attributes = True