from sqlalchemy.ext.asyncio import create_async_engine
from collections.abc import AsyncGenerator
from sqlalchemy import text
from ...core.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
import uuid


engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=settings.DEBUG,
    pool_size= 20,
    max_overflow=10,
    pool_pre_ping=True
    
)
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def set_tenant_context(session: AsyncSession, institution_id: uuid.UUID) -> None:
    """Sets the PostgreSQL session-local tenant variable for RLS enforcement."""
    await session.execute(
        text("SET LOCAL app.current_institution_id = :inst_id"),
        {"inst_id": str(institution_id)},
    )


class Base(DeclarativeBase):
    pass