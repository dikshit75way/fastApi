from fastapi import UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.modules.project.service import (
    create_project, 
    get_all_projects, 
    get_project_by_id, 
    update_project as service_update_project, 
    delete_project as service_delete_project,
    attach_zip_to_project
)
from app.modules.project.schema import ProjectBase
from app.core.storage import save_zip_file, save_image_file

class ProjectController:
    
    @staticmethod
    async def create_project(
        title: str,
        description: str,
        price: int,
        file: UploadFile,
        images: List[UploadFile],
        db: AsyncSession,
        current_user: dict
    ):
        # Save the ZIP file first
        print("debbug the file data form the frontend :", file)
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

    @staticmethod
    async def get_all_projects(db: AsyncSession):
        return await get_all_projects(db)

    @staticmethod
    async def get_project_by_id(project_id: int, db: AsyncSession):
        return await get_project_by_id(db, project_id)

    @staticmethod
    async def update_project(
        project_id: int, 
        payload: ProjectBase, 
        db: AsyncSession, 
        current_user: dict
    ):
        return await service_update_project(db, project_id, payload, current_user.get("user_id"))

    @staticmethod
    async def delete_project(
        project_id: int, 
        db: AsyncSession, 
        current_user: dict
    ):
        return await service_delete_project(db, project_id, current_user.get("user_id"))

    @staticmethod
    async def upload_project_zip(
        project_id: int, 
        file: UploadFile, 
        db: AsyncSession, 
        current_user: dict
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
