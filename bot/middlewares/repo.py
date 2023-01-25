from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from bot.service.repo.base import SQLAlchemyRepo


class Repository(BaseMiddleware):
    def __init__(self, async_factory: AsyncSession) -> None:
        super().__init__()
        self.async_factory = async_factory

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        async with self.async_factory() as _session:
            data['repo'] = SQLAlchemyRepo(_session)

            result = await handler(event, data)

            data.pop('repo')

            return result

