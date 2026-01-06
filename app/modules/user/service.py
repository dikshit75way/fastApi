from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.modules.user.models import User
from app.core.security import hash_password , verify_password
from app.modules.user.validation import validate_sufficient_balance, validate_user_exists
from fastapi import HTTPException, status

async def create_user(db:AsyncSession , name : str , email : str , password:str, role: str = "user", wallet_balance: int = 500):
    user = User(
        name=name, 
        email=email, 
        hashed_password=hash_password(password),
        role=role,
        wallet_balance=wallet_balance
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_email(db:AsyncSession , email : str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user and user.wallet_balance is None:
        user.wallet_balance = 0
    return user

    return user
