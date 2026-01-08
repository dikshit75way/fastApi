from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.reviews.service import create_review as service_create_review, get_reviews as service_get_reviews
from app.modules.reviews.validation import validate_review_ownership
from app.modules.reviews.schema import ReviewCreate
from app.core.jwt import user_required
from fastapi import HTTPException , status , Depends 

class ReviewController:
    
    @staticmethod
    async def create_review(db:AsyncSession , payload : ReviewCreate , current_user:dict = Depends(user_required)):
        validate_review_ownership(payload.user_id, current_user.get("user_id"))
        result = await service_create_review(db , payload)
        return {"message":"Review created successfully" , "data":result}

    @staticmethod
    async def get_reviews(db:AsyncSession , project_id : int ):
        if project_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid project id")
        reviews = await service_get_reviews(db , project_id)
        return {"message":"Reviews fetched successfully" , "data":reviews}

    

