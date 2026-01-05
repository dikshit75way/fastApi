from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from app.modules.purchase.model import Purchase
from app.modules.project.model import Project
from app.modules.purchase.schema import PurchaseCreate
from app.modules.purchase.validation import validate_purchase_not_self
from app.modules.project.validation import validate_project_exists
from fastapi import HTTPException, status
from app.modules.user.service import debit_wallet , credit_wallet
from app.modules.wallet.service import create_wallet_transaction

async def create_purchase(db:AsyncSession, payload:PurchaseCreate):
    admin_id = 7
    project = await validate_project_exists(db, payload.project_id)
    validate_purchase_not_self(project, payload.buyer_id)

    commissionRate = 0.1 
    commission = int(project.price * commissionRate)
    seller_amount = project.price - commission

    # debit_wallet handles its own internal validation (funds check)
    await debit_wallet(db, payload.buyer_id, project.price)
    
    purchase_record = Purchase(
        buyer_id=payload.buyer_id,
        project_id=payload.project_id,
        amount=project.price,
        commission=commission,
        status="purchased"
    )
    db.add(purchase_record)
    
    await credit_wallet(db, project.owner_id, seller_amount)
    await credit_wallet(db, admin_id, commission)
    
    walletpayload = {
        "buyer_id": payload.buyer_id,
        "seller_id": project.owner_id,
        "admin_id": admin_id,
        "purchase_id": purchase_record.id,
        "amount": project.price,
        "commission": commission
    }
    await create_wallet_transaction(db, walletpayload)
    
    await db.commit()
    await db.refresh(purchase_record)
    return purchase_record

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
