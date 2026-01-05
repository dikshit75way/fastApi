from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.project.model import Project
from app.modules.project.schema import ProjectBase
from app.modules.project.validation import validate_project_exists, validate_project_owner

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
    return await validate_project_exists(db, project_id)

async def update_project(db: AsyncSession, project_id: int, payload: ProjectBase, user_id: int):
    project = await validate_project_exists(db, project_id)
    validate_project_owner(project, user_id)

    project.title = payload.title
    project.description = payload.description
    project.price = payload.price
    project.zip_path = payload.zip_path
    
    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project_id: int, user_id: int):
    project = await validate_project_exists(db, project_id)
    validate_project_owner(project, user_id)
    
    await db.delete(project)
    await db.commit()
    return {"message": "deleted successfully", "project_id": project_id}

async def attach_zip_to_project(
    db: AsyncSession,
    project_id: int,
    user_id: int,
    zip_path: str
):
    project = await validate_project_exists(db, project_id)
    validate_project_owner(project, user_id)

    project.zip_path = zip_path
    await db.commit()
    await db.refresh(project)

    return project
