
from celery.schedules import crontab


from bot.service.workflow.worker import celery
from .ext.anniversary_tasks import sync_date_engine, chain_sender_anniversary


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
	print('vrv')
	sender.add_periodic_task(
		crontab(hour=0, minute=0, day_of_month="5"),
		sync_date_engine.s(),
		name='sync_employment_data_from_gsheets',
	)

	sender.add_periodic_task(
		crontab(hour=9, minute=0),
		chain_sender_anniversary.s(),
		name="send_anniversary_for_personal"
	)

	#test tasks
	# sender.add_periodic_task(
	# 	20.0,
	# 	chain_sender_anniversary.s(),
	# 	name="send_anniversary_for_personal"
	# )



