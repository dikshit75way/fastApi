from fastapi import APIRouter , Depends , status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.reviews.schema import ReviewCreate , ReviewOut
from app.core.jwt import user_required
from typing import List
from app.modules.reviews.controller import ReviewController

router = APIRouter(prefix="/reviews" , tags=["reviews"])

@router.post("/" , response_model=ReviewOut , status_code=status.HTTP_201_CREATED)
async def post_review(
    payload:ReviewCreate,
    db:AsyncSession = Depends(get_db),
    current_user:dict = Depends(user_required)
 ):
  return await ReviewController.create_review(db , payload , current_user)

@router.get("/{project_id}" , response_model=List[ReviewOut])
async def list_reviews(
    project_id: int,
    db:AsyncSession = Depends(get_db)
):
 return await ReviewController.get_reviews(db , project_id)