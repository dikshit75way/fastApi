from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.user.schema import UserCreate, UserOut, LoginRequest, LoginResponse, RefreshTokenRequest
from app.core.database import get_db
from app.core.jwt import user_required
from app.modules.user.controller import UserController

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    # Map 'username' (from Swagger/OAuth2) to 'email' associated with your business logic
    login_data = await UserController.login(
        db,
        form_data.username,
        form_data.password
    )
    # Return standard OAuth2 response for Swagger UI
    return {
        "access_token": login_data["accessToken"],
        "token_type": "bearer",
        "refresh_token": login_data["refreshToken"]
    }

@router.post("/register", response_model=LoginResponse)
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserController.create_user(
        db, 
        user_data.name, 
        user_data.email, 
        user_data.password, 
        user_data.role, 
        user_data.wallet_balance
    )

@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await UserController.login(
        db, 
        payload.email, 
        payload.password
    )

@router.post("/refresh-token", response_model=LoginResponse)
async def refresh_token(payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
   return await UserController.refresh_token(payload, db)

@router.get("/me", response_model=UserOut)
async def get_current_user_info(
    current_user: dict = Depends(user_required),
    db: AsyncSession = Depends(get_db)
):  
    print(f"current user : {current_user}")
    return await UserController.get_current_user_info(current_user, db)
