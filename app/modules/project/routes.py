from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from typing import List
from app.modules.project.service import (
    create_project, 
    get_all_projects, 
    get_project_by_id, 
    update_project, 
    delete_project ,
    attach_zip_to_project
)
from app.core.jwt import user_required
from app.modules.project.schema import ProjectOut, ProjectBase 
from app.core.storage import save_zip_file, save_image_file

router = APIRouter(prefix="/project", tags=["project"])

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
    # Save the ZIP file first
    zip_path = save_zip_file(file)

    # Validate and save images
    image_paths = []
    if images:
        if len(images) > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum 5 images allowed"
            )
        for img in images:
            path = save_image_file(img)
            image_paths.append(path)
    
    # Create the project with the zip_path and image_paths
    return await create_project(
        db, 
        title, 
        description, 
        price, 
        current_user.get("user_id"), 
        zip_path,
        image_paths
    )

@router.get("/", response_model=list[ProjectOut])
async def get_all_projects_endpoint(
    db: AsyncSession = Depends(get_db)
):
    return await get_all_projects(db)

@router.get("/{project_id}", response_model=ProjectOut)
async def get_project_by_id_endpoint(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_project_by_id(db, project_id)

@router.put("/{project_id}", response_model=ProjectOut)
async def update_project_endpoint(
    project_id: int,
    payload: ProjectBase,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    return await update_project(db, project_id, payload, current_user.get("user_id"))

@router.delete("/{project_id}")
async def delete_project_endpoint(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    return await delete_project(db, project_id, current_user.get("user_id"))


@router.post("/{project_id}/upload")
async def upload_project_zip(
    project_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    zip_path = save_zip_file(file)

    project = await attach_zip_to_project(
        db=db,
        project_id=project_id,
        user_id=current_user["user_id"],
        zip_path=zip_path
    )

    return {
        "message": "ZIP uploaded successfully",
        "project_id": project.id,
        "zip_path": project.zip_path
    }