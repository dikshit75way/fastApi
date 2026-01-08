from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.core.jwt import user_required
from app.modules.purchase.schema import PurchaseCreate, PurchaseOut
from app.modules.purchase.controller import PurchaseController

router = APIRouter(prefix="/purchases", tags=["purchases"])

@router.get("/has-purchased", response_model=bool)
async def check_has_purchased(
    project_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await PurchaseController.has_purchased(db, project_id, user_id)

@router.post("/", response_model=PurchaseOut, status_code=status.HTTP_201_CREATED)
async def buy_project(
    payload: PurchaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
   
    
    return await PurchaseController.buy_project(payload , db , current_user)

@router.get("/", response_model=List[PurchaseOut])
async def list_my_purchases(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    return await PurchaseController.list_my_purchases(db , current_user)