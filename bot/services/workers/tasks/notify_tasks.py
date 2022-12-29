import asyncio

from aiogram import Bot
from aiogram import exceptions, loggers

from bot.config_reader import config
from bot.models.member import MemberPydantic
from bot.services.workers import celery
from bot.templates.text import to_notify


SENDER_TIMEOUT = 0.3

@celery.task()
def send_notify_for_admins(member: MemberPydantic, type_update: str):
    asyncio.run(send_notify_update(member=member, type_update=type_update))

async def send_notify_update(member: MemberPydantic, type_update: str):
    bot = Bot(config.bot_token, parse_mode="HTML")
    text = await to_notify.get_notify_text(member, type_update)
    admins = await bot.get_chat_administrators(chat_id=config.channel_id)

    for admin in admins:
        try:
            await bot.send_message(chat_id=admin.user.id, text=text)
            await asyncio.sleep(SENDER_TIMEOUT)
        except exceptions.TelegramRetryAfter:
            loggers.event.info(
                f"Custom log - module:{__name__} - f'Достигнут лимит на отправку сообщений'")
        except exceptions.TelegramAPIError:
            loggers.event.info(
                f"Custom log - module:{__name__} - f'Target [ID:{admin.user.id}]: failed'")

    await bot.session.close()

