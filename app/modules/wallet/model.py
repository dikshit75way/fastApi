
from sqlalchemy import Column , Integer , String , ForeignKey , DateTime
from app.core.database import Base
from sqlalchemy.sql import func


class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)
    reference_id = Column(Integer, nullable=False)
    source = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
