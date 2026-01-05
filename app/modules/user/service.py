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
    return result.scalars().first()

async def debit_wallet(db:AsyncSession , use_id : int , amount : int):
    stmt = (
        update(User)
        .where(User.id == use_id, User.wallet_balance >= amount)
        .values(wallet_balance=User.wallet_balance - amount)
        .returning(User)
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    validate_sufficient_balance(bool(user))
    
    await db.commit()
    return user


async def credit_wallet(
    db: AsyncSession,
    user_id: int,
    amount: int
):
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid amount"
        )

    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(wallet_balance=User.wallet_balance + amount)
        .returning(User)
    )

    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await db.commit()
    return user
