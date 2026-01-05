from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.wallet.model import Wallet
from app.modules.wallet.schema import WalletCreate
from fastapi import HTTPException, status

async def create_wallet_transaction(db: AsyncSession, payload: dict):
    """
    Creates multiple wallet records for a single purchase.
    Expects payload with: buyer_id, seller_id, admin_id, purchase_id, amount, commission
    """
    records = [
        # Debit for buyer
        Wallet(
            user_id=payload["buyer_id"],
            type="debit",
            reference_id=payload["purchase_id"],
            source="purchase",
            amount=payload["amount"]
        ),
        # Credit for seller
        Wallet(
            user_id=payload["seller_id"],
            type="credit",
            reference_id=payload["purchase_id"],
            source="withdraw",
            amount=payload["amount"] - payload["commission"]
        ),
        # Credit for admin (commission)
        Wallet(
            user_id=payload["admin_id"],
            type="credit",
            reference_id=payload["purchase_id"],
            source="commission",
            amount=payload["commission"]
        )
    ]
    
    db.add_all(records)
    # Note: caller handles commit
    return records

async def get_transactions(db: AsyncSession, user_id: int):
    result = await db.execute(select(Wallet).where(Wallet.user_id == user_id))
    transactions = result.scalars().all()
    print("debugging the result: ", transactions)
    return transactions