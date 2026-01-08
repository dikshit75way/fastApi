from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.jwt import user_required
from app.modules.payment.schema import PaymentSessionCreate, PaymentSessionOut
from app.modules.payment.controller import PaymentController

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/create-session", response_model=PaymentSessionOut)
async def create_payment_session(
    payload: PaymentSessionCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(user_required)
):
    user_id = current_user.get("user_id")
    # We don't need to recreate payload if it's already validated, 
    # but keeping logic similar to before to accept user input
    return await PaymentController.create_payment_session(
        payload, db, current_user
    )


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None),
    db: AsyncSession = Depends(get_db)
):
    payload = await request.body()
    return await PaymentController.verify_webhook(payload, stripe_signature, db)

   
