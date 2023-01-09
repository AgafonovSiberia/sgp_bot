
from bot.services.workers.celery_worker import celery
from bot.services.workers.tasks.ext.sync_tasks import sync_employment_date_from_gsheets


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
	sender.add_periodic_task(20.0, sync_employment_date_from_gsheets.s(), name='sync_employment_data_from_gsheets')
		#5го числа каждого месяца
		# crontab(0, 0, day_of_month='5')

