from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import  DeclarativeBase
from app.core.config import settings

DATABASE_URI = settings.DATABASE_URL

class Base(DeclarativeBase):
    pass

engine = create_async_engine(DATABASE_URI, echo=settings.DEBUG)
AsyncSessionLocal = async_sessionmaker(engine , expire_on_commit=False)

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
        print("Database connection connected..")
    finally:
        await db.close()
