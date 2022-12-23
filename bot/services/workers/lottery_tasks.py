from aiogram import Bot

from bot.config_reader import config
from bot.services.methods.lottery_methods import ticket_factory
from bot.services.workers.celery_worker import celery
import asyncio


@celery.task()
def generate_lottery_ticket(data_config: dict, user_id: int):
        bot = Bot(config.bot_token, parse_mode="HTML")
        result = asyncio.run(ticket_factory(data_config=data_config, user_id=user_id, bot=bot))
        await bot.close()
        return result

