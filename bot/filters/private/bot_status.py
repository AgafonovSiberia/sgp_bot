from aiogram import Bot, types
from aiogram.dispatcher.filters import BaseFilter
from aiogram.exceptions import TelegramForbiddenError
from aiogram.methods.get_chat_member import GetChatMember

from bot.config_reader import config

class BotStatusFilter(BaseFilter):
    bot_added: bool

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        bot = await bot.get_me()
        status = False
        try:
            member = await GetChatMember(chat_id=config.channel_id, user_id=bot.id)
            status = True if member.status == "administrator" else False
        except TelegramForbiddenError:
            print("Bot is not a member of the methods chat")
        return status == self.bot_added
