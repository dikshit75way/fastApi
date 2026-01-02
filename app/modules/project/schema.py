from pydantic import BaseModel

from typing import Optional

class ProjectBase(BaseModel):
    title: str
    description: str
    price: int
    zip_path: Optional[str] = None

class ProjectOut(BaseModel):
    id: int
    title: str
    description: str
    price: int
    owner_id: int
    zip_path: Optional[str] = None
    
    class Config:
        from_attributes = True