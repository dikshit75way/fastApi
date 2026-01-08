import stripe
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException , status , Depends
from app.modules.wallet.service import credit_funds as service_credit_funds
from app.modules.payment.schema import PaymentSessionCreate
from app.modules.payment.service import create_checkout_session as service_create_payment_session , verify_webhook as service_verify_webhook
from app.core.jwt import user_required


from app.modules.purchase.service import fulfill_stripe_purchase

class PaymentController:

    @staticmethod
    async def create_payment_session(payload : PaymentSessionCreate , db:AsyncSession , current_user:dict= Depends(user_required)):
        user_id = current_user.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user id")
        
        # The service expects individual arguments, not the payload object directly
        result = await service_create_payment_session(
            user_id=user_id,
            amount=payload.amount,
            success_url=payload.success_url,
            cancel_url=payload.cancel_url
        )
        return {"message":"Payment session created successfully" , "data":result}


    @staticmethod
    async def verify_webhook(payload: bytes, sig_header: str, db: AsyncSession):
        if not payload or not sig_header:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload or signature header")
        event = await service_verify_webhook(payload, sig_header)
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            metadata = session.get("metadata", {})
            event_type = metadata.get("type")

            if event_type == "wallet_topup":
                user_id = int(metadata.get("user_id"))
                amount = session.get("amount_total")
                await service_credit_funds(db, user_id, amount, source="stripe_topup")
                await db.commit()
        
            elif event_type == "project_purchase":
                purchase_id = int(metadata.get("purchase_id"))
                await fulfill_stripe_purchase(db, purchase_id)

        return {"status": "success"}