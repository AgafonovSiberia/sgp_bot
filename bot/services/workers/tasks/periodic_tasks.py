import asyncio
from celery.schedules import crontab
from aiogram import Bot, exceptions, loggers
from datetime import datetime as dt
from sqlalchemy.ext.asyncio import AsyncSession


from bot.google_sheets_api.gsheets_api import get_worksheet, WORKSHEET
from bot.db.engine import create_async_session
from bot.services.repo.base import SQLAlchemyRepo
from bot.services.repo import MemberRepo
from bot.services.repo.ext import CongratulationRepo
from bot.services.workers.celery_worker import celery

from bot.config_reader import config

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
	sender.add_periodic_task(
		crontab(hour=0, minute=0, day_of_month="5"),
		sync_employment_date_from_gsheets.s(),
		name='sync_employment_data_from_gsheets'
	)

	sender.add_periodic_task(
		crontab(hour=9, minute=0),
		send_anniversary.s(),
		name="send_anniversary_for_personal"
	)


@celery.task
def sync_employment_date_from_gsheets():
	"""Синхронизирует даты приёма на работу из гугл-таблицы в базу данных"""
	asyncio.run(sync_date_engine())
async def sync_date_engine():
	worksheet = get_worksheet(WORKSHEET.BASIC_IDX)
	#[2:] - срезает первые строки, отведённые под заголовок
	users_id= worksheet.col_values(1)[2:]
	users_employment_date =[dt.strptime(elem, "%d.%m.%Y").date() if elem else None
							for elem in worksheet.col_values(13)[2:]]

	async_session: AsyncSession = await create_async_session()
	async with async_session() as _session:
		repo = SQLAlchemyRepo(_session)
		for user_id, employment_date in zip(users_id, users_employment_date):
			await repo.get_repo(MemberRepo).update_employment_date(user_id=int(user_id),
																   employment_date=employment_date)


@celery.task
def send_anniversary():
	"""Рассылает поздравления работникам-юбилярам(от даты приёма на работу)"""
	asyncio.run(send_anniversary_engine())

async def send_anniversary_engine():
	async_session: AsyncSession = await create_async_session()
	async with async_session() as _session:
		repo = SQLAlchemyRepo(_session)
		members = await repo.get_repo(MemberRepo).get_member_is_anniversary()
		if not members:
			return

		bot = Bot(config.bot_token, parse_mode="HTML")
		for member in members:
			try:
				current_year_anniversary = dt.now().year - int(member[1])
				template = await repo.get_repo(CongratulationRepo).get_congratulation_data(slot_id=current_year_anniversary)
				if template:
					await bot.send_photo(chat_id=member[0], photo=template.img_id, caption=template.caption)

			except exceptions.TelegramRetryAfter:
				loggers.event.info(
					f"Custom log - module:{__name__} - f'Достигнут лимит на отправку сообщений'")
			except exceptions.TelegramAPIError:
				loggers.event.info(
					f"Custom log - module:{__name__} - f'Target [ID:{member[0]}]: failed'")

		await bot.session.close()



