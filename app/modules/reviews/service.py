from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from app.modules.reviews.model import Review
from app.modules.project.validation import validate_project_exists
from app.modules.reviews.schema import ReviewCreate
from app.modules.purchase.service import has_purchased
from fastapi import HTTPException, status

async def create_review(db:AsyncSession , payload:ReviewCreate):
    # Check if project exists in Projects table
    await validate_project_exists(db, payload.project_id)
    
    # Check if user has purchased the project
    if not await has_purchased(db, payload.project_id, payload.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You must purchase the project before leaving a review"
        )
    
    # Create the review
    review = Review(**payload.model_dump())
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review


async def get_reviews(db:AsyncSession , project_id:int):
    result = await db.execute(select(Review).where(Review.project_id == project_id))
    return result.scalars().all()
