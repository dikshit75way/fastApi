import stripe
from app.core.config import settings
from app.modules.payment.schema import PaymentSessionCreate
from fastapi import HTTPException

stripe.api_key = settings.STRIPE_SECRET_KEY

async def create_checkout_session(
    user_id: int, 
    amount: int, 
    success_url: str, 
    cancel_url: str, 
    product_name: str = "Wallet Top-up",
    metadata: dict = {}
):
    try:
        # Defaults for metadata
        session_metadata = {
            "user_id": str(user_id),
            "type": "wallet_topup"
        }
        session_metadata.update(metadata)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": product_name,
                        },
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=session_metadata
        )
        return {
            "session_id": session.id,
            "checkout_url": session.url
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def verify_webhook(payload: bytes, sig_header: str):
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        return event
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
