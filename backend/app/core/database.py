"""
Database Configuration
"""
import asyncpg
from typing import Optional
from app.core.config import settings

db_pool: Optional[asyncpg.Pool] = None


async def init_db():
    """Initialize database connection pool"""
    global db_pool
    db_pool = await asyncpg.create_pool(settings.DATABASE_URL)
    print("Database connection pool initialized")


async def get_db():
    """Get database connection from pool"""
    if db_pool is None:
        raise RuntimeError("Database not initialized")
    async with db_pool.acquire() as conn:
        yield conn


async def close_db():
    """Close database connection pool"""
    global db_pool
    if db_pool:
        await db_pool.close()
        print("Database connection pool closed")
