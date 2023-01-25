import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.core import core_router
from bot.extension import extensions_router

from bot.database.base import Base
from bot.middlewares.repo import Repository

from bot.extension.setup import setup_extensions

from bot.config_reader import config


logger = logging.getLogger(__name__)



def setup_middlewares(async_session):
    extensions_router.message.outer_middleware(Repository(async_factory=async_session))
    extensions_router.callback_query.outer_middleware(Repository(async_factory=async_session))

    core_router.message.outer_middleware(Repository(async_factory=async_session))
    core_router.callback_query.outer_middleware(Repository(async_factory=async_session))
    core_router.chat_member.outer_middleware(Repository(async_factory=async_session))
    core_router.chat_join_request.outer_middleware(Repository(async_factory=async_session))

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        stream=sys.stdout)

    logger.info("Starting bot")

    bot = Bot(config.bot_token, parse_mode="HTML")
    storage = MemoryStorage()

    engine = create_async_engine(config.POSTGRES_URL, future=True, echo=False)

    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_factory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    dp = Dispatcher(storage=storage)

    setup_middlewares(async_session=async_factory)

    await setup_extensions(extensions_router=extensions_router, async_factory=async_factory)

    dp.include_router(core_router)
    dp.include_router(extensions_router)


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
