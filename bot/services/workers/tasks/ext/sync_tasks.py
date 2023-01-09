import asyncio
from datetime import datetime as dt
from sqlalchemy.ext.asyncio import AsyncSession


from bot.google_sheets_api.gsheets_api import get_worksheet, WORKSHEET
from bot.db.engine import create_async_session
from bot.services.repo.base import SQLAlchemyRepo
from bot.services.repo import MemberRepo
from bot.services.workers.celery_worker import celery



@celery.task
def sync_employment_date_from_gsheets():
	"""Синхронизируем дату приёма на работу из гугл-таблицы в базу данных"""
	asyncio.run(sync_date_engine())
async def sync_date_engine():
	worksheet = get_worksheet(WORKSHEET.BASIC_IDX)
	#[2:] - срезает первые строки, отведённые под заголовок
	users_id= worksheet.col_values(1)[2:]
	users_employment_date =[dt.strptime(elem, "%d.%m.%Y").date() if elem else None
							for elem in worksheet.col_values(13)[2:]]

	async_session: AsyncSession = await create_async_session()
	async with async_session() as session:
		repo = SQLAlchemyRepo(session)
		for user_id, employment_date in zip(users_id, users_employment_date):
			await repo.get_repo(MemberRepo).update_employment_date(user_id=int(user_id),
																   employment_date=employment_date)


