"""
Async SQLAlchemy database connection.

Supports:
  - PostgreSQL (production / Docker)
  - SQLite (local development — no install needed)
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from .config import settings
from ..models.base import Base


# ── Choose engine based on database URL ─────────────────────────────────

def _build_engine():
    """Create the right engine for the database URL."""
    url = settings.DATABASE_URL

    # SQLite needs aiosqlite for async support
    if url.startswith("sqlite"):
        return create_async_engine(
            url,
            echo=settings.DEBUG,
            connect_args={"check_same_thread": False},
        )
    else:
        # PostgreSQL / other databases
        return create_async_engine(
            url,
            echo=settings.DEBUG,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
        )


engine = _build_engine()

# ── Session Factory ─────────────────────────────────────────────────────

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ── FastAPI Dependency ──────────────────────────────────────────────────

async def get_db() -> AsyncSession:
    """
    Yields an async database session.
    Used as a FastAPI dependency:

        @router.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...
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


# ── Table Creation ──────────────────────────────────────────────────────

async def create_tables():
    """Create all tables — use Alembic in production."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
