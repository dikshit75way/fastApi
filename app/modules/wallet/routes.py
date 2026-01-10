from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.wallet.schema import WalletOut, Widhdraw, WalletAdd
from app.core.jwt import user_required
from typing import List
from app.modules.wallet.controller import walletController


router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.post("/add" , response_model=WalletOut)
async def add_funds(
    payload : WalletAdd,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    return await walletController.credit_wallet_balance(db, current_user.get("user_id") , payload.amount)

@router.post("/withdraw" , response_model=WalletOut)
async def withdraw(
    payload : Widhdraw,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    return await walletController.withdraw(db, current_user.get("user_id") , payload.amount)

@router.get("/history", response_model=List[WalletOut])
async def list_transactions(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    print("we are hititng the list_transactions routes")
    return await walletController.list_transactions(db, current_user.get("user_id"))
