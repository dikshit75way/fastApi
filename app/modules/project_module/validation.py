from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.project_module.model import ProjectModule
from app.modules.project.service import get_project_by_id as get_project

async def validate_project_module_exists(db: AsyncSession, project_module_id: int, owner_id: int) -> ProjectModule:
    """
    Validates that a project module exists and that the provided owner_id 
    is the owner of the project associated with this module.
    """
    result = await db.execute(
        select(ProjectModule).where(ProjectModule.id == project_module_id)
    )
    project_module = result.scalar_one_or_none()
    
    if not project_module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Project module not found"
        )
    
    # Verify ownership via the parent project service
    project = await get_project(db, project_module.project_id)
    
    if project.owner_id != owner_id:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to modify this project module"
        )
        
    return project_module
