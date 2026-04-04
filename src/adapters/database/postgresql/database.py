from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

from src.config.settings import settings as db_settings

engine = create_async_engine(
    db_settings.database_url,
    echo=False,
    future=True,
    pool_size=db_settings.POSTGRES_POOL_SIZE,
    max_overflow=db_settings.POSTGRES_MAX_OVERFLOW,
    pool_timeout=db_settings.POSTGRES_POOL_TIMEOUT,
    connect_args={"command_timeout": db_settings.POSTGRES_COMMAND_TIMEOUT}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
