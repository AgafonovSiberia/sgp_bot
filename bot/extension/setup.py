from aiogram import Router
from sqlalchemy.ext.asyncio import AsyncSession
from bot.service.repo.ext import SettingsRepo
from bot.service.repo.base import SQLAlchemyRepo
from bot.service.workflow.tasks.gsheets_tasks import create_sheets_to_extensions
from bot.misc.states import Extension


from .lottery.handlers import extension_lottery_router
from .anniversary.handlers import anniversary_admin_router

async def set_primary_module_settings(repo: SQLAlchemyRepo):
	for ext in Extension:
		check = await repo.get_repo(SettingsRepo).check_modules_settings(module_name=Extension.anniversary.name)
		if check:
			continue

		await repo.get_repo(SettingsRepo).add_module_settings(module_name=ext.name,
                                                              is_active=False,
                                                              module_config=ext.primary_config(name=ext.name))

	create_sheets_to_extensions.delay()






async def setup_extensions(extensions_router: Router, async_factory:AsyncSession):
	extensions_router.include_router(extension_lottery_router)
	extensions_router.include_router(anniversary_admin_router)
	async with async_factory() as _session:
		repo = SQLAlchemyRepo(_session)
		await set_primary_module_settings(repo=repo)






