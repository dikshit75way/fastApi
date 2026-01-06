from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProjectImageOut(BaseModel):
    id: int
    image_path: str
    created_at: datetime

    class Config:
        from_attributes = True

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
    created_at: datetime
    images: List[ProjectImageOut] = []
    
    class Config:
        from_attributes = True