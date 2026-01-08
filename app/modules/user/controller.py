from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.user.service import (
    create_user as service_create_user, 
    authenticate_user as service_authenticate_user, 
    get_user_by_id as service_get_user_by_id,
    get_user_by_email as service_get_user_by_email
)
from app.core.jwt import create_access_token, create_refresh_token, verify_access_token
from app.modules.user.schema import RefreshTokenRequest, UserOut
from app.modules.user.validation import validate_user_exists

class UserController:
    
    @staticmethod
    async def create_user(
        db: AsyncSession,
        name: str,
        email: str,
        password: str,
        role: str,
        wallet_balance: int
    ):
        if not name or not email or not password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user data")
        
        user = await service_create_user(db, name, email, password, role, wallet_balance)
        
        token_data = {"user_id": user.id, "role": user.role}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        return {
            "user": user, 
            "accessToken": access_token, 
            "refreshToken": refresh_token
        }

    @staticmethod
    async def login(db: AsyncSession, email: str, password: str):
        if not email or not password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password")
        
        user = await service_authenticate_user(db, email, password)
        if not user:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token_data = {"user_id": user.id, "role": user.role}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        return {
            "user": user, 
            "accessToken": access_token, 
            "refreshToken": refresh_token
        }

    @staticmethod
    async def refresh_token(payload: RefreshTokenRequest, db: AsyncSession):
        refresh_token = payload.refreshToken
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token")
        
        decoded = verify_access_token(refresh_token)
        if not decoded or decoded.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
        user_id = decoded.get("user_id")
        user = await service_get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        token_data = {"user_id": user.id, "role": user.role}
        access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)
        
        return {
            "user": user, 
            "accessToken": access_token, 
            "refreshToken": new_refresh_token
        }

    @staticmethod
    async def get_current_user_info(current_user: dict, db: AsyncSession):
        print("current user" , current_user)
        user = await service_get_user_by_id(db, current_user.get("user_id"))
        print("user is found or not " , user)
        validate_user_exists(user)
        return user