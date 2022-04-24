
from aiogram.dispatcher.filters import BaseFilter
from aiogram import types
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from typing import Union, List

from aiogram.methods.get_chat_member import GetChatMember

from bot import channel_config


class BotStatusFilter(BaseFilter):
    bot_added: bool

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        bot = await bot.get_me()
        status = False
        try:
            member = await GetChatMember(chat_id=channel_config.channel_id, user_id=bot.id)
            status = True if member.status == "administrator" else False
            print("status", status)
        except TelegramForbiddenError:
            print("Bot is not a member of the methods chat")
        return status == self.bot_added
