from aiogram import Bot

from bot import channel_config
from bot.models.member import MemberPydantic


async def send_notify(member: MemberPydantic, bot: Bot, type_update: str):
    text = await notify_texts.get_notify_text(member, type_update)
    admins = await bot.get_chat_administrators(chat_id=channel_config.channel_id)
    for admin in admins:
        try:
            await bot.send_message(chat_id=admin.user.id, text=text)
        except Exception as e:
            print(str(e))
