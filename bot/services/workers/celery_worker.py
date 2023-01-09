from celery import Celery
from bot.config_reader import config



celery = Celery("web", broker=config.REDIS_URI,
                backend=config.REDIS_URI,
                include=["bot.services.workers.tasks.gsheets_tasks",
                         "bot.services.workers.tasks.notify_tasks",
                         "bot.services.workers.tasks.ext.lottery_tasks",
                         "bot.services.workers.tasks.ext.sync_tasks"])


class CeleryConfig:
    task_serializer = "pickle"
    result_serializer = "pickle"
    event_serializer = "json"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]
    timezone = "UTC"

#
# celery.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'bot.services.workers.tasks.ext.sync_tasks.sync_data_from_gsheets',
#         'schedule': 3.0,
#     },
# }



celery.config_from_object(CeleryConfig)

