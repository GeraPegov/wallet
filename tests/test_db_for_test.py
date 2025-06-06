import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.pool import NullPool

from app.core.database import Base
from app.core.models import Wallet
from app.repositories.wallet_manager import WalletManager


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///./test.db")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession)
    async with AsyncSessionLocal() as session:
        yield session

# test_db_for_test.py
@pytest.mark.asyncio
async def test_add_wallet(db_session):
    wallet_manager = WalletManager(db_session)
    example_wallet_id = '123qwe456q'
    await wallet_manager.add_wallet(example_wallet_id)
    
    # Проверяем, что данные добавились
    result = await db_session.execute(select(Wallet))
    assert result.scalars().first().wallet_id == example_wallet_id