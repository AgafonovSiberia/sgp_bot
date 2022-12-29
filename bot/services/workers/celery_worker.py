from celery import Celery
from bot.config_reader import config
from bot.google_sheets_api.gsheets_api import get_worksheet, WORKSHEET
import asyncio
from aiogram import Bot


celery = Celery("web", broker=config.REDIS_URI,
                backend=config.REDIS_URI,
                include=["bot.services.workers.tasks.gsheets_tasks",
                         "bot.services.workers.tasks.notify_tasks",
                         "bot.services.workers.tasks.ext.lottery_tasks"])
class CeleryConfig:
    task_serializer = "pickle"
    result_serializer = "pickle"
    event_serializer = "json"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]


celery.config_from_object(CeleryConfig)


