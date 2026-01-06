from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from fastapi import HTTPException, status
from app.modules.reviews.model import Review
from app.modules.project.model import Project
from app.modules.project.validation import validate_project_exists
from app.modules.reviews.schema import ReviewCreate
from app.modules.purchase.service import has_purchased

async def create_review(db: AsyncSession, payload: ReviewCreate):
    # 1️⃣ Check if project exists
    await validate_project_exists(db, payload.project_id)
    
    # 2️⃣ Check if user has purchased the project
    if not await has_purchased(db, payload.project_id, payload.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must purchase the project before leaving a review"
        )
    
    # 3️⃣ Create the review
    review = Review(**payload.model_dump())
    db.add(review)
    await db.commit()
    await db.refresh(review)

    # 4️⃣ Calculate avg_rating and count for this project
    stmt = (
        select(
            func.avg(Review.rating).label("avg_rating"),
            func.count(Review.id).label("count")
        )
        .where(Review.project_id == payload.project_id)
    )
    result = await db.execute(stmt)
    stats = result.first()  # Like stats[0] in Mongo

    if stats:
        avg_rating, count = stats.avg_rating, stats.count
        # Update Project table
        await db.execute(
            update(Project)
            .where(Project.id == payload.project_id)
            .values(avg_rating=avg_rating, rating_count=count)
        )
        await db.commit()

    return review


async def get_reviews(db: AsyncSession, project_id: int):
    result = await db.execute(select(Review).where(Review.project_id == project_id))
    return result.scalars().all()
