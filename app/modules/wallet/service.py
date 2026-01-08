from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException, status

from app.modules.user.models import User
from app.modules.wallet.model import Wallet


# ------------------------
# CREDIT FUNDS
# ------------------------
async def credit_funds(
    db: AsyncSession,
    user_id: int,
    amount: int,
    source: str,
    reference_id: int = 0
):
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid amount for credit"
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

    transaction = Wallet(
        user_id=user_id,
        type="credit",
        reference_id=reference_id,
        source=source,
        amount=amount
    )

    db.add(transaction)
    return transaction


# ------------------------
# DEBIT FUNDS
# ------------------------
async def debit_funds(
    db: AsyncSession,
    user_id: int,
    amount: int,
    source: str,
    reference_id: int = 0
):
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid amount for debit"
        )

    stmt = (
        update(User)
        .where(User.id == user_id, User.wallet_balance >= amount)
        .values(wallet_balance=User.wallet_balance - amount)
        .returning(User)
    )

    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        user_check = await db.execute(
            select(User).where(User.id == user_id)
        )
        if not user_check.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )

    transaction = Wallet(
        user_id=user_id,
        type="debit",
        reference_id=reference_id,
        source=source,
        amount=amount
    )

    db.add(transaction)
    return transaction


# ------------------------
# GET TRANSACTIONS (READ ONLY)
# ------------------------
async def get_transactions(db: AsyncSession, user_id: int):
    print("🔥 get_transactions service hit")
    result = await db.execute(
        select(Wallet).where(Wallet.user_id == user_id)
    )
    return result.scalars().all()


# ------------------------
# WITHDRAW
# ------------------------
async def user_withdraw(db: AsyncSession, user_id: int, amount: int):
    transaction = await debit_funds(db, user_id, amount, "withdraw")
    return transaction


# ------------------------
# CREDIT WALLET (DEPOSIT)
# ------------------------
async def credit_wallet_balance(db: AsyncSession, user_id: int, amount: int):
    if amount <= 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be greater than 100"
        )

    transaction = await credit_funds(db, user_id, amount, "deposit")
    return transaction


# ------------------------
# ATOMIC PURCHASE TRANSACTION
# ------------------------
async def create_wallet_transaction(db: AsyncSession, payload: dict):
    async with db.begin():
        await debit_funds(
            db,
            payload["buyer_id"],
            payload["amount"],
            "purchase",
            payload["purchase_id"]
        )

        await credit_funds(
            db,
            payload["seller_id"],
            payload["amount"] - payload["commission"],
            "withdraw",
            payload["purchase_id"]
        )

        await credit_funds(
            db,
            payload["admin_id"],
            payload["commission"],
            "commission",
            payload["purchase_id"]
        )

    return True
