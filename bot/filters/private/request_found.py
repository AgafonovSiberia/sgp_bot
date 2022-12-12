from aiogram import types
from aiogram.dispatcher.filters import BaseFilter

from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.services.repo.request_repo import RequestRepo


class RequestIsFoundFilter(BaseFilter):
    request_is_found: bool

    async def __call__(self, message: types.Message, repo: SQLAlchemyRepo) -> bool:
        check_request = await repo.get_repo(RequestRepo).check_request(message.chat.id)
        return check_request == self.request_is_found
