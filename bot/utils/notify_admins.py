from aiogram import Bot

from bot.config_reader import config
from bot.models.member import MemberPydantic
from bot.templates.text import notify_text


async def send_notify_update(member: MemberPydantic, bot: Bot, type_update: str):
    text = await notify_text.get_notify_text(member, type_update)
    admins = await bot.get_chat_administrators(chat_id=config.channel_id)
    for admin in admins:
        try:
            await bot.send_message(chat_id=admin.user.id, text=text)
        except Exception as e:
            print(str(e))

async def send_notify_defender(bot: Bot, type_update: str):
    pass



