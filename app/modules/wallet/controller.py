from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends

from app.core.jwt import user_required
from app.modules.wallet.service import (
    get_transactions as service_get_transactions,
    user_withdraw as service_user_withdraw,
    credit_wallet_balance as service_credit_wallet_balance
)
from app.modules.wallet.schema import Widhdraw, WalletAdd


class walletController:

    @staticmethod
    async def credit_wallet_balance(
        payload: WalletAdd,
        db: AsyncSession,
        current_user: dict = Depends(user_required)
    ):
        try:
            user_id = current_user.get("user_id")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid user id"
                )

            transaction = await service_credit_wallet_balance(
                db, user_id, payload.amount
            )

            await db.commit()
            await db.refresh(transaction)

            return {
                "message": "Wallet balance updated successfully",
                "data": transaction
            }

        except HTTPException:
            await db.rollback()
            raise

        except Exception as e:
            await db.rollback()
            print("🔥 credit_wallet_balance error:", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to credit wallet balance"
            )


    @staticmethod
    async def withdraw(
        payload: Widhdraw,
        db: AsyncSession,
        current_user: dict = Depends(user_required)
    ):
        try:
            user_id = current_user.get("user_id")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid user id"
                )

            transaction = await service_user_withdraw(
                db, user_id, payload.amount
            )

            await db.commit()
            await db.refresh(transaction)

            return {
                "message": "Withdrawal successful",
                "data": transaction
            }

        except HTTPException:
            await db.rollback()
            raise

        except Exception as e:
            await db.rollback()
            print("🔥 withdraw error:", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Withdrawal failed"
            )


    @staticmethod
    async def list_transactions(
        db: AsyncSession,
        current_user: dict = Depends(user_required)
    ):
        try:
            print("🔥 list_transactions controller hit")

            user_id = current_user.get("user_id")
            print("user_id:", user_id)

            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid user id"
                )

            transactions = await service_get_transactions(db, user_id)

            return {
                "message": "Transactions fetched successfully",
                "data": transactions
            }

        except HTTPException:
            raise

        except Exception as e:
            print("🔥 list_transactions error:", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch transactions"
            )
