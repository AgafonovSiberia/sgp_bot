from aiogram.dispatcher.filters import BaseFilter
from aiogram import types

from typing import Union, List


class LinkCreatorFilter(BaseFilter):
    link_creator: Union[None, List[str], str]

    async def __call__(self, update: types.ChatMemberUpdated) -> bool:

        creator_status = "not_link"
        if update.invite_link:
            creator_status = "bot" if update.invite_link.creator.is_bot else "administrator"
        else:
            creator_status = "not_link_user" if update.from_user.id == update.new_chat_member.user.id else "not_link_administrator"
        return creator_status in self.link_creator
