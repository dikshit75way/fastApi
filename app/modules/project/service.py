from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.project.model import Project
from app.modules.project.schema import ProjectBase
from fastapi import HTTPException, status

async def create_project(db: AsyncSession, title: str, description: str, price: int, user_id: int, zip_path: str):
    project = Project(
        title=title,
        description=description,
        price=price,
        owner_id=user_id,
        zip_path=zip_path
    )

    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def get_all_projects(db:AsyncSession):
    result = await db.execute(select(Project))
    return result.scalars().all()


async def get_project_by_id(db:AsyncSession , project_id:int):
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()

async def update_project(db: AsyncSession, project_id: int, payload: ProjectBase, user_id: int):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    if project.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this project")

    project.title = payload.title
    project.description = payload.description
    project.price = payload.price
    project.zip_path = payload.zip_path
    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project_id: int, user_id: int):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    if project.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this project")
    
    await db.delete(project)
    await db.commit()
    return {"message": "deleted successfully", "project_id": project_id}

async def attach_zip_to_project(
    db: AsyncSession,
    project_id: int,
    user_id: int,
    zip_path: str
):
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not project owner")

    project.zip_path = zip_path
    await db.commit()
    await db.refresh(project)

    return project
