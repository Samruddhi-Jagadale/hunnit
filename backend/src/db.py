from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings
import os

# -----------------------------------------
# SETTINGS
# -----------------------------------------
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://pguser:password@db:5432/hunnit_db"

    class Config:
        env_file = ".env"

settings = Settings()

# -----------------------------------------
# DATABASE
# -----------------------------------------
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
