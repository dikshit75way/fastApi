from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.user.schema import UserCreate, UserOut, LoginRequest, LoginResponse, RefreshTokenRequest
from app.modules.user.service import create_user, authenticate_user, get_user_by_id
from app.modules.user.validation import validate_user_exists
from app.core.database import get_db
from app.core.jwt import create_access_token, create_refresh_token, verify_access_token, user_required

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=LoginResponse)
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await create_user(
        db, 
        user_data.name, 
        user_data.email, 
        user_data.password, 
        user_data.role, 
        user_data.wallet_balance
    )
    
    token_data = {"user_id": user.id, "role": user.role}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return { 
        "user" : user, 
        "accessToken": access_token, 
        "refreshToken": refresh_token
    }

@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token_data = {"user_id": user.id, "role": user.role}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return { 
        "user" : user, 
        "accessToken": access_token, 
        "refreshToken": refresh_token
    }

@router.post("/refresh-token", response_model=LoginResponse)
async def refresh_token(payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    decoded = verify_access_token(payload.refreshToken)
    if not decoded or decoded.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    user_id = decoded.get("user_id")
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    token_data = {"user_id": user.id, "role": user.role}
    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)
    
    return {
        "user": user,
        "accessToken": new_access_token,
        "refreshToken": new_refresh_token
    }

@router.get("/me", response_model=UserOut)
async def get_current_user_info(
    current_user: dict = Depends(user_required),
    db: AsyncSession = Depends(get_db)
):
    """Protected route - returns current authenticated user's information"""
    user = await get_user_by_id(db, current_user.get("user_id"))
    validate_user_exists(user)
    return user
