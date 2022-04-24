from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.repo.base.repository import SQLAlchemyRepo


class Repository(BaseMiddleware):
    def __init__(self, async_session: AsyncSession) -> None:
        super().__init__()
        self.async_session = async_session

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        async with self.async_session() as session:
            data['repo'] = SQLAlchemyRepo(session)

            result = await handler(event, data)

            data.pop('repo')

            return result

