from app.modules.user.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.modules.wallet.model import Wallet
from app.modules.wallet.schema import WalletCreate
from fastapi import HTTPException, status

async def credit_funds(db: AsyncSession, user_id: int, amount: int, source: str, reference_id: int = 0):
    """
    Centralized, atomic function to credit funds to a user's wallet.
    Automatically creates a ledger entry in the wallets table.
    """
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid amount for credit"
        )

    # Atomic update to user balance
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

    # Create history record
    transaction = Wallet(
        user_id=user_id,
        type="credit",
        reference_id=reference_id,
        source=source,
        amount=amount
    )
    db.add(transaction)
    
    # Note: caller should handle overall transaction commit unless it's a standalone call
    return transaction

async def debit_funds(db: AsyncSession, user_id: int, amount: int, source: str, reference_id: int = 0):
    """
    Centralized, atomic function to debit funds from a user's wallet.
    Ensures balance doesn't go below zero (Insufficient balance).
    Automatically creates a ledger entry in the wallets table.
    """
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid amount for debit"
        )

    # Atomic update with balance check
    stmt = (
        update(User)
        .where(User.id == user_id, User.wallet_balance >= amount)
        .values(wallet_balance=User.wallet_balance - amount)
        .returning(User)
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        # Check if user exists but just has insufficient balance
        user_check = await db.execute(select(User).where(User.id == user_id))
        if not user_check.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )

    # Create history record
    transaction = Wallet(
        user_id=user_id,
        type="debit",
        reference_id=reference_id,
        source=source,
        amount=amount
    )
    db.add(transaction)
    
    return transaction

async def create_wallet_transaction(db: AsyncSession, payload: dict):
    """
    Legacy helper for backward compatibility during refactor.
    """
    await debit_funds(db, payload["buyer_id"], payload["amount"], "purchase", payload["purchase_id"])
    await credit_funds(db, payload["seller_id"], payload["amount"] - payload["commission"], "withdraw", payload["purchase_id"])
    await credit_funds(db, payload["admin_id"], payload["commission"], "commission", payload["purchase_id"])
    return True

async def get_transactions(db: AsyncSession, user_id: int):
    result = await db.execute(select(Wallet).where(Wallet.user_id == user_id))
    transactions = result.scalars().all()
    return transactions

async def user_withdraw(db: AsyncSession, user_id: int, amount: int):
    transaction = await debit_funds(db, user_id, amount, "withdraw")
    await db.commit()
    await db.refresh(transaction)
    return transaction

async def credit_wallet_balance(db: AsyncSession, user_id: int, amount: int):
    if amount <= 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be greater than 100")
    
    transaction = await credit_funds(db, user_id, amount, "deposit")
    await db.commit()
    await db.refresh(transaction)
    return transaction
    




    