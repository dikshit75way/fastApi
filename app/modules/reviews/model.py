from sqlalchemy import Column , Integer , String , ForeignKey , DateTime
from app.core.database import Base
from sqlalchemy.sql import func

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer , primary_key=True , index=True)
    user_id = Column(Integer , ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer , ForeignKey("projects.id"), nullable=False)
    rating = Column(Integer , nullable=False)
    comment = Column(String , nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
