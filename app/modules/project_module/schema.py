from pydantic import BaseModel 
from datetime import datetime

class ProjectModuleBase(BaseModel):
    project_id : int 
    name : str 
    description : str 

class ProjectModuleCreate(ProjectModuleBase):
    pass

class ProjectModuleOut(BaseModel):
    id : int 
    project_id : int 
    name : str 
    description : str 
    created_at : datetime

    class Config:
        from_attributes = True