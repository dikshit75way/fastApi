from fastapi import HTTPException, status

def validate_purchase_not_self(project_owner_id: int, buyer_id: int):
    if project_owner_id == buyer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="You cannot purchase your own project"
        )
