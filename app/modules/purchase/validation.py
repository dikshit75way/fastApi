from fastapi import HTTPException, status
from app.modules.project.model import Project

def validate_purchase_not_self(project: Project, buyer_id: int):
    if project.owner_id == buyer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="You cannot purchase your own project"
        )
