from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from app.modules.purchase.model import Purchase
from app.modules.purchase.schema import PurchaseCreate
from app.modules.purchase.validation import validate_purchase_not_self
from app.modules.project.service import get_project_by_id as get_project
from fastapi import HTTPException, status
from app.modules.payment.service import create_checkout_session
from app.modules.wallet.service import debit_funds, credit_funds

async def create_purchase(db:AsyncSession, payload:PurchaseCreate):
    admin_id = 7
    project = await get_project(db, payload.project_id)
    validate_purchase_not_self(project.owner_id, payload.buyer_id)

    commissionRate = 0.1 
    commission = int(project.price * commissionRate)
    seller_amount = project.price - commission

    # Create purchase record (default to pending if stripe)
    purchase_record = Purchase(
        buyer_id=payload.buyer_id,
        project_id=payload.project_id,
        amount=project.price,
        commission=commission,
        status="purchased" if payload.payment_method == "wallet" else "pending"
    )
    db.add(purchase_record)
    await db.flush() # Flush to get purchase_record.id

    if payload.payment_method == "wallet":
        # 1. Debit buyer
        await debit_funds(db, payload.buyer_id, project.price, source="purchase", reference_id=purchase_record.id)
        
        # 2. Credit seller
        await credit_funds(db, project.owner_id, seller_amount, source="sale", reference_id=purchase_record.id)
        
        # 3. Credit admin (commission)
        await credit_funds(db, admin_id, commission, source="commission", reference_id=purchase_record.id)
        
        await db.commit()
        await db.refresh(purchase_record)
        return purchase_record
    
    else:
        # STRIPE FLOW
        # Note: We don't credit seller/admin yet. Webhook will do it.
        session = await create_checkout_session(
            user_id=payload.buyer_id,
            amount=project.price, # price in smallest unit
            success_url="http://localhost:3000/success", # In real app, these come from frontend
            cancel_url="http://localhost:3000/cancel",
            product_name=f"Purchase: {project.title}",
            metadata={
                "type": "project_purchase",
                "purchase_id": str(purchase_record.id),
                "project_id": str(project.id),
                "seller_id": str(project.owner_id)
            }
        )
        await db.commit() # Save pending purchase
        
        # Return purchase record with checkout_url added
        purchase_record.checkout_url = session["checkout_url"]
        return purchase_record

async def fulfill_stripe_purchase(db: AsyncSession, purchase_id: int):
    """
    Called by Stripe Webhook to complete the purchase and distribute funds.
    """
    admin_id = 7
    result = await db.execute(select(Purchase).where(Purchase.id == purchase_id))
    purchase = result.scalar_one_or_none()

    if not purchase or purchase.status == "purchased":
        return

    project = await get_project(db, purchase.project_id)
    seller_id = project.owner_id
    seller_amount = purchase.amount - purchase.commission

    # Update status
    purchase.status = "purchased"

    # Credit seller
    await credit_funds(db, seller_id, seller_amount, source="sale", reference_id=purchase.id)
    
    # Credit admin
    await credit_funds(db, admin_id, purchase.commission, source="commission", reference_id=purchase.id)
    
    await db.commit()
    return purchase

async def get_purchases(db: AsyncSession, user_id: int):
    result = await db.execute(select(Purchase).where(Purchase.buyer_id == user_id))
    return result.scalars().all()


async def has_purchased(db:AsyncSession , project_id : int , user_id : int ) -> bool:
    stmt = select(exists().where(
        Purchase.project_id == project_id, 
        Purchase.buyer_id == user_id, 
        Purchase.status == "purchased"
    ))
    result = await db.execute(stmt)
    return result.scalar()
