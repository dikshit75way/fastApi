from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.jwt import user_required
from app.modules.purchase.schema import PurchaseCreate, PurchaseOut
from app.modules.purchase.service import create_purchase, get_purchases

router = APIRouter(prefix="/purchases", tags=["purchases"])

@router.post("/", response_model=PurchaseOut, status_code=status.HTTP_201_CREATED)
async def buy_project(
    payload: PurchaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    """
    Purchase a project. Ensure the buyer_id in payload matches current_user.
    """
    if payload.buyer_id != current_user.get("user_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only purchase projects for yourself."
        )
    return await create_purchase(db, payload)

@router.get("/", response_model=List[PurchaseOut])
async def list_my_purchases(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    """
    List all projects purchased by the current user.
    """
    return await get_purchases(db, current_user.get("user_id"))