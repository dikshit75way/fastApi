from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from app.modules.project_module.model import ProjectModule
from app.modules.project_module.schema import ProjectModuleBase
from app.modules.project_module.validation import validate_project_module_exists
from app.modules.project.validation import validate_project_exists
from fastapi import HTTPException, status

async def create_project_module(db:AsyncSession , payload:ProjectModuleBase):
    project = await validate_project_exists(db, payload.project_id)
    project_module = ProjectModule(**payload.model_dump())
    db.add(project_module)
    await db.commit()
    await db.refresh(project_module)
    return project_module

async def get_all_project_modules(db:AsyncSession):
    result = await db.execute(select(ProjectModule))
    return result.scalars().all()


async def delete_project_module(db:AsyncSession , project_module_id:int , owner_id:int):
    project_module = await validate_project_module_exists(db, project_module_id, owner_id)
    await db.delete(project_module)
    await db.commit()
    return {"message": "deleted successfully", "project_module_id": project_module_id}