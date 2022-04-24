
from sqlalchemy.ext.asyncio import AsyncSession
from functools import lru_cache
from typing import Type, TypeVar

from bot.services.repo.base.base_repository import BaseSQLAlchemyRepo


T = TypeVar("T", bound=BaseSQLAlchemyRepo)


class SQLAlchemyRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    @lru_cache()
    def get_repo(self, repo: Type[T]) -> T:
        return repo(self._session)

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
