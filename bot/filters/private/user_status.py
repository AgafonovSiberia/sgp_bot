from aiogram.dispatcher.filters import BaseFilter
from aiogram import types

from typing import Union, List
from bot import channel_config
from aiogram.methods.get_chat_member import GetChatMember


class StatusUserFilter(BaseFilter):
    status_user: Union[str, List[str]]
    
    async def __call__(self, message: types.Message) -> bool:
        member = await GetChatMember(chat_id=channel_config.channel_id, user_id=message.chat.id)
        print("member", member)
        return member.status in self.status_user
