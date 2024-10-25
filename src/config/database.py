from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

UserBase = declarative_base()

DATABASE_URL = 'postgresql+asyncpg://postgres:password@localhost:5432/UserDB'

engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(class_=AsyncSession, bind=engine)


async def get_user_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
