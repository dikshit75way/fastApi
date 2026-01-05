from sqlalchemy import Column , Integer , String , ForeignKey , DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class ProjectModule(Base):
    __tablename__ = "project_modules"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    