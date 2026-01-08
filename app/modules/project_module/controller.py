from fastapi import HTTPException , status , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.jwt import user_required
from app.modules.project_module.service import create_project_module as service_create_project_module , get_all_project_modules as service_get_all_project_modules , delete_project_module as service_delete_project_module
from app.modules.project_module.schema import ProjectModuleCreate

class ProjectModuleController:
    
    @staticmethod
    async def create_project_module(payload : ProjectModuleCreate , db:AsyncSession , current_user:dict= Depends(user_required)):
        user_id = current_user.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user id")
        result = await service_create_project_module(db , user_id , payload)
        return {"message":"Project module created successfully" , "data":result}
    
    @staticmethod
    async def get_all_project_modules(db:AsyncSession , current_user:dict= Depends(user_required)):
        user_id = current_user.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user id")
        result = await service_get_all_project_modules(db , user_id)
        return {"message":"Project modules fetched successfully" , "data":result}
    
    @staticmethod
    async def delete_project_module(db:AsyncSession , current_user:dict= Depends(user_required)):
        user_id = current_user.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user id")
        result = await service_delete_project_module(db , user_id)
        return {"message":"Project module deleted successfully" , "data":result}