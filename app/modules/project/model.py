from sqlalchemy import Column, String, Integer, ForeignKey
from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    zip_path = Column(String(255), nullable=True)

    
    
