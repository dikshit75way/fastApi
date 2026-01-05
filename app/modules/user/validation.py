from fastapi import HTTPException, status
from app.modules.user.models import User

def validate_user_exists(user: User):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

def validate_sufficient_balance(success: bool):
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Insufficient balance or user not found"
        )
