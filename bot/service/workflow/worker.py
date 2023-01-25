from celery import Celery
from celery.beat import PersistentScheduler
from bot.config_reader import config


celery = Celery("web",
                broker=config.REDIS_URL,
                backend=config.REDIS_URL,
                include=["bot.service.workflow.tasks.periodic_tasks",
                         "bot.service.workflow.tasks.gsheets_tasks",
                         "bot.service.workflow.tasks.notify_tasks",
                         "bot.service.workflow.tasks.ext.lottery_tasks",
                         "bot.service.workflow.tasks.ext.anniversary_tasks"
                         ])


class CeleryConfig:
    task_serializer = "pickle"
    result_serializer = "pickle"
    event_serializer = "json"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]
    timezone = "Europe/Moscow"




celery.config_from_object(CeleryConfig)

