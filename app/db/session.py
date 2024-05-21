from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from app.config import DATABASE_URL_SESSION


engine = create_async_engine(
    DATABASE_URL_SESSION,
    future=True,
    echo=True
)
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
