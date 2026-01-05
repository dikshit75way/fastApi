from fastapi import APIRouter , Depends , status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.reviews.schema import ReviewCreate , ReviewOut
from app.modules.reviews.service import create_review as service_create_review, get_reviews
from app.modules.reviews.validation import validate_review_ownership
from app.core.jwt import user_required
from typing import List

router = APIRouter(prefix="/reviews" , tags=["reviews"])

@router.post("/" , response_model=ReviewOut , status_code=status.HTTP_201_CREATED)
async def post_review(
    payload:ReviewCreate,
    db:AsyncSession = Depends(get_db),
    current_user:dict = Depends(user_required)
 ):
    validate_review_ownership(payload.user_id, current_user.get("user_id"))
    return await service_create_review(db , payload)

@router.get("/{project_id}" , response_model=List[ReviewOut])
async def list_reviews(
    project_id: int,
    db:AsyncSession = Depends(get_db)
):
    return await get_reviews(db , project_id)