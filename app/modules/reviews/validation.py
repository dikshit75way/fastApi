from fastapi import HTTPException, status

def validate_review_ownership(review_user_id: int, current_user_id: int):
    if review_user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Cannot post review for another user"
        )
