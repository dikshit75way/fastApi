from sqlalchemy import Column, String, Integer, ForeignKey , DateTime
from sqlalchemy import func
from app.core.database import Base

from sqlalchemy.orm import relationship

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    zip_path = Column(String(255), nullable=True)
    avgRating = Column(Integer, nullable=True , default=0)
    ratingCount = Column(Integer, nullable=True , default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to multiple images
    images = relationship("ProjectImage", back_populates="project", cascade="all, delete-orphan")

class ProjectImage(Base):
    __tablename__ = "project_images"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    image_path = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="images")
