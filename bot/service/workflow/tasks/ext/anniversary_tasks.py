from datetime import datetime as dt
from celery import chain

from aiogram import Bot, exceptions, loggers

from sqlalchemy.ext.asyncio import AsyncSession

from bot.external_api.gsheets_api import get_worksheet, WORKSHEET
from bot.utils.async_session import create_async_session
from bot.service.repo.base import SQLAlchemyRepo
from bot.service.repo import MemberRepo
from bot.service.repo.ext import AnniversaryRepo, SettingsRepo
from bot.service.workflow.worker import celery

from bot.misc.states import Extension
from bot.config_reader import config

from bot.service.workflow.task_utils import asyncio_celery_task_runner


@celery.task
def chain_sender_anniversary():
	"""Цепочка задач по рассылке поздравлений"""
	chain_list = chain(check_sender_is_active.s(), send_anniversary.s())
	chain_list.delay()

@celery.task
@asyncio_celery_task_runner
async def check_sender_is_active() -> None | list[tuple]:
	"""Проверяет активирована ли рассылка поздравлений"""
	async_session: AsyncSession = create_async_session()
	async with async_session() as _session:
		repo = SQLAlchemyRepo(_session)
		anniversary_sender_is_active = await repo.get_repo(SettingsRepo).module_is_active(Extension.anniversary.name)

		if not anniversary_sender_is_active:
			return None

		members = await repo.get_repo(MemberRepo).get_member_is_anniversary()
		return members


@celery.task
@asyncio_celery_task_runner
async def send_anniversary(members: list[tuple]):
	"""
	Рассылка поздравлений пользователям
	:param members: список кортежей [(user_id, employment_year), (user_id, employment_year), ...]
	"""
	if not members:
		return

	async_session: AsyncSession = create_async_session()
	async with async_session() as _session:
		repo = SQLAlchemyRepo(_session)
		bot = Bot(config.bot_token, parse_mode="HTML")

		for member in members:
			current_year_anniversary = dt.now().year - int(member[1])
			template = await repo.get_repo(AnniversaryRepo).get_congratulation_data(slot_id=current_year_anniversary)
			if template:
				try:
					await bot.send_photo(chat_id=member[0], photo=template.img_id, caption=template.caption)
				except exceptions.TelegramRetryAfter:
					loggers.event.info("Лимит на отправку сообщений'")

				except exceptions.TelegramAPIError:
					loggers.event.info(f"Target [ID:{member[0]}]: failed'")

		await bot.session.close()


@celery.task
@asyncio_celery_task_runner
async def sync_date_engine():
	"""Синхронизируем даты приёма на работу GoogleSheet -> Database"""
	worksheet = get_worksheet(WORKSHEET.BASIC_IDX)
		#[2:] - срезает 2 строки(заголовки)
	users_id_list= worksheet.col_values(1)[2:]
	employment_date_list =[dt.strptime(elem, "%d.%m.%Y").date()
						   if elem else None
						   for elem in worksheet.col_values(13)[2:]
						   ]

	async_session: AsyncSession = create_async_session()
	async with async_session() as _session:
		repo = SQLAlchemyRepo(_session)
		for user_id, employment_date in zip(users_id_list, employment_date_list):
			await repo.get_repo(MemberRepo).update_employment_date(
				user_id=int(user_id), employment_date=employment_date)




