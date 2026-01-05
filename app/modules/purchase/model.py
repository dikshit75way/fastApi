from sqlalchemy import Column, Integer, DateTime, ForeignKey , String
from sqlalchemy.sql import func
from app.core.database import Base

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)

    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    commission = Column(Integer, nullable=False, default=0)
    status = Column(String(255), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
