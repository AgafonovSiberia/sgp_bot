
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from bot.config_reader import config

def create_async_session():
    engine = create_async_engine(f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
                             f"@db:5432/{config.POSTGRES_DB}",
                             future=True, echo=False)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return async_session