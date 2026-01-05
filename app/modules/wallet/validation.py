from fastapi import HTTPException, status

def validate_positive_amount(amount: int):
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Amount must be positive"
        )
