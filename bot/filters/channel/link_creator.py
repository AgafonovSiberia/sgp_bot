from aiogram.dispatcher.filters import BaseFilter
from aiogram import types

from typing import Union, List


class LinkCreatorFilter(BaseFilter):
    link_creator: str

    async def __call__(self, update: types.ChatMemberUpdated) -> bool:

        creator_status = "not_bot"
        if update.invite_link:
            creator_status = "bot" if update.invite_link.creator.is_bot else "not_bot"
        return creator_status == self.link_creator
