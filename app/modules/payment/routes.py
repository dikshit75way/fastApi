from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.jwt import user_required
from app.modules.payment.schema import PaymentSessionCreate, PaymentSessionOut
from app.modules.payment.service import create_checkout_session, verify_webhook
from app.modules.wallet.service import credit_funds
import stripe

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/create-session", response_model=PaymentSessionOut)
async def create_payment_session(
    payload: PaymentSessionCreate, 
    current_user: dict = Depends(user_required)
):
    user_id = current_user.get("user_id")
    return await create_checkout_session(
        user_id=user_id,
        amount=payload.amount,
        success_url=payload.success_url,
        cancel_url=payload.cancel_url
    )

from app.modules.purchase.service import fulfill_stripe_purchase

@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None),
    db: AsyncSession = Depends(get_db)
):
    payload = await request.body()
    event = verify_webhook(payload, stripe_signature)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata", {})
        event_type = metadata.get("type")

        if event_type == "wallet_topup":
            user_id = int(metadata.get("user_id"))
            amount = session.get("amount_total")
            await credit_funds(db, user_id, amount, source="stripe_topup")
            await db.commit()
        
        elif event_type == "project_purchase":
            purchase_id = int(metadata.get("purchase_id"))
            await fulfill_stripe_purchase(db, purchase_id)

    return {"status": "success"}
