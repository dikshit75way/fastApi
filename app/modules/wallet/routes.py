from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.wallet.service import get_transactions, user_withdraw, credit_wallet_balance
from app.modules.wallet.schema import WalletOut, Widhdraw, WalletAdd
from app.core.jwt import user_required
from typing import List


router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.post("/add" , response_model=WalletOut)
async def add_funds(
    payload : WalletAdd,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    return await credit_wallet_balance(db, current_user.get("user_id") , payload.amount)

@router.post("/withdraw" , response_model=WalletOut)
async def withdraw(
    payload : Widhdraw,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    return await user_withdraw(db, current_user.get("user_id") , payload.amount)

@router.get("/history", response_model=List[WalletOut])
async def list_transactions(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    return await get_transactions(db, current_user.get("user_id"))
