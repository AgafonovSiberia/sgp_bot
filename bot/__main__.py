import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.handlers.member_update import member_update_router
from bot.handlers.admin import admin_router
from bot.handlers.registration import registration_router
from bot.handlers.user import user_router

from bot.db.base import Base
from bot.middlewares.repo import Repository


from bot.config_reader import config
from celery import Celery

logger = logging.getLogger(__name__)




async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        stream=sys.stdout)

    logger.info("Starting bot")

    bot = Bot(config.bot_token, parse_mode="HTML")
    storage = MemoryStorage()



    engine = create_async_engine(f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
        f"@db:5432/{config.POSTGRES_DB}",
                                 future=True, echo=False)

    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    dp = Dispatcher(storage=storage)

    """private routers"""
    registration_router.message.outer_middleware(Repository(async_session=async_session))

    admin_router.message.outer_middleware(Repository(async_session=async_session))
    admin_router.callback_query.outer_middleware(Repository(async_session=async_session))

    member_update_router.chat_join_request.outer_middleware(Repository(async_session=async_session))
    member_update_router.chat_member.outer_middleware(Repository(async_session=async_session))

    user_router.message.outer_middleware(Repository(async_session=async_session))
    user_router.callback_query.outer_middleware(Repository(async_session=async_session))

    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.include_router(registration_router)
    dp.include_router(member_update_router)



    try:
        await bot.get_updates(offset=-1)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Exit")
