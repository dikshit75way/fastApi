from fastapi import HTTPException , status , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.purchase.schema import PurchaseCreate
from app.modules.purchase.service import (
    get_purchases as service_get_purchases, 
    has_purchased as service_has_purchased, 
    create_purchase as service_create_purchase
)
from app.core.jwt import user_required


class PurchaseController:
    
    @staticmethod
    async def buy_project(payload : PurchaseCreate , db:AsyncSession , current_user:dict= Depends(user_required)):
        if payload.buyer_id != current_user.get("user_id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only purchase projects for yourself."
            )
        
        result = await service_create_purchase(db , payload)
        return {"message":"Project purchased successfully" , "data":result}

    @staticmethod
    async def list_my_purchases(db :AsyncSession , current_user:dict= Depends(user_required)):
        user_id = current_user.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user id")
        purchases = await service_get_purchases(db , user_id)
        return {"message":"Purchases fetched successfully" , "data":purchases}

    @staticmethod
    async def has_purchased(db:AsyncSession , project_id : int , user_id : int):
        if project_id is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid project id or user id")
        result = await service_has_purchased(db , project_id , user_id)
        return {"message":"Purchase checked successfully" , "data":result}

    
        
       
