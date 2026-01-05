from sqlalchemy import Column, String, Integer
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    wallet_balance = Column(Integer, default=500)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # user/admin
