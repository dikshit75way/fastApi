from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.wallet.service import get_transactions
from app.modules.wallet.schema import WalletOut
from app.core.jwt import user_required
from typing import List

router = APIRouter(prefix="/wallets", tags=["wallets"])

@router.get("/history", response_model=List[WalletOut])
async def list_transactions(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    return await get_transactions(db, current_user.get("user_id"))
