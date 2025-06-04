from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
#конфигурацию лучше хранить в отдельном файле
SQL_DB_URL = 'postgresql+asyncpg://postgres:2710@localhost/postgres'

async_engine = create_async_engine(SQL_DB_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()
