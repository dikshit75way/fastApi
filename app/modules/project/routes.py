from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from typing import List
from app.modules.project.controller import ProjectController
from app.core.jwt import user_required
from app.modules.project.schema import ProjectOut, ProjectBase 


router = APIRouter(prefix="/projects", tags=["project"])

@router.post("/", response_model=ProjectOut)
async def create_project_endpoint(
    title: str = Form(...),
    description: str = Form(...),
    price: int = Form(...),
    file: UploadFile = File(...),
    images: List[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    return await ProjectController.create_project(
        title, 
        description, 
        price, 
        file, 
        images, 
        db, 
        current_user
    )

@router.get("/", response_model=list[ProjectOut])
async def get_all_projects_endpoint(
    db: AsyncSession = Depends(get_db)
):
    return await ProjectController.get_all_projects(db)

@router.get("/{project_id}", response_model=ProjectOut)
async def get_project_by_id_endpoint(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await ProjectController.get_project_by_id(project_id, db)

@router.put("/{project_id}", response_model=ProjectOut)
async def update_project_endpoint(
    project_id: int,
    payload: ProjectBase,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    return await ProjectController.update_project(project_id, payload, db, current_user)

@router.delete("/{project_id}")
async def delete_project_endpoint(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    return await ProjectController.delete_project(project_id, db, current_user)


@router.post("/{project_id}/upload")
async def upload_project_zip(
    project_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    return await ProjectController.upload_project_zip(project_id, file, db, current_user)