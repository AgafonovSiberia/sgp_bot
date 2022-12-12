from typing import Union, List

from aiogram import types
from aiogram.dispatcher.filters import BaseFilter
from aiogram.methods.get_chat_member import GetChatMember

from bot.config_reader import config



class StatusUserFilter(BaseFilter):
    status_user: Union[str, List[str]]
    async def __call__(self, message: types.Message) -> bool:
        member = await GetChatMember(chat_id=config.channel_id, user_id=message.chat.id)
        return member.status in self.status_user
