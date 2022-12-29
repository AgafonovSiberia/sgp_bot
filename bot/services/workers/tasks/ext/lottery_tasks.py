
from bot.services.methods.lottery_methods import ticket_factory
from bot.services.workers.celery_worker import celery
import asyncio


@celery.task()
def generate_lottery_ticket(data_config: dict, user_id: int):
        result = asyncio.run(ticket_factory(data_config=data_config, user_id=user_id))
        return result

