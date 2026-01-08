from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException , status , Depends
from app.core.jwt import user_required
from app.modules.wallet.service import get_transactions as service_get_transactions , user_withdraw as service_user_withdraw , credit_wallet_balance as service_credit_wallet_balance
from app.modules.wallet.schema import Widhdraw , WalletAdd

class walletController:

    @staticmethod
    async def get_wallet_balance(payload : WalletAdd , db:AsyncSession , current_user:dict = Depends(user_required)):
        user_id = current_user.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user id")
        result = await service_credit_wallet_balance(db , user_id , payload.amount)
        return {"message":"Wallet balance updated successfully" , "data":result}


    @staticmethod
    async def withdraw(payload : Widhdraw , db:AsyncSession , current_user:dict = Depends(user_required)):
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user id")

        result = await service_user_withdraw(db , user_id , payload.amount)
        return {"message":"Withdrawal successful" , "data":result}
        
    @staticmethod
    async def list_transactions(db:AsyncSession , current_user:dict = Depends(user_required)):
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user id")
        result = await service_get_transactions(db , user_id)
        return {"message":"Transactions fetched successfully" , "data":result}
