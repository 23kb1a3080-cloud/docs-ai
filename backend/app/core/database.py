"""
Database configuration and session management
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

from app.core.config import settings

# Convert database URL for async driver
db_url = settings.DATABASE_URL
if db_url.startswith("sqlite"):
    # Use aiosqlite for async SQLite
    db_url = db_url.replace("sqlite:///", "sqlite+aiosqlite:///")
    # Create async engine for SQLite (no pool settings)
    engine = create_async_engine(
        db_url,
        echo=settings.DEBUG,
    )
elif db_url.startswith("postgresql://"):
    # Use asyncpg for PostgreSQL
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
    # Create async engine for PostgreSQL (with pool settings)
    engine = create_async_engine(
        db_url,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        echo=settings.DEBUG,
    )
else:
    # Default engine
    engine = create_async_engine(
        db_url,
        echo=settings.DEBUG,
    )

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create declarative base
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
