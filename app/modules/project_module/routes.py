from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.project_module.schema import ProjectModuleCreate
from app.modules.project_module.controller import ProjectModuleController


router = APIRouter(prefix="/modules", tags=["project_module"])

@router.post("/", response_model=ProjectModuleCreate)
async def create_project_module_endpoint(
    payload: ProjectModuleCreate,
    db: AsyncSession = Depends(get_db),
):
    return await ProjectModuleController.create_project_module(payload , db)

@router.get("/", response_model=list[ProjectModuleCreate])
async def get_all_project_modules_endpoint(
    db: AsyncSession = Depends(get_db)
):
    return await ProjectModuleController.get_all_project_modules(db)


@router.delete("/{project_module_id}")
async def delete_project_module_endpoint(
    project_module_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await ProjectModuleController.delete_project_module(db, project_module_id)


