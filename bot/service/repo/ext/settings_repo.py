from bot.service.repo.base.repository import BaseSQLAlchemyRepo
from bot.database.models import ModuleSettings
from sqlalchemy import select, update, func
from bot.misc.states import Extension


class SettingsRepo(BaseSQLAlchemyRepo):
    async def add_module_settings(self, module_name: str, module_config: dict,
                                  is_active: bool = False):
        await self._session.merge(ModuleSettings(module_name=module_name,
                                                 is_active=is_active,
                                                 module_config=module_config))
        await self._session.commit()


    async def get_module_settings(self, module_name: str):
        settings = await self._session.execute(select(ModuleSettings).
                                               where(ModuleSettings.module_name == module_name))
        return settings.scalar()

    async def check_modules_settings(self, module_name: str):
        record = await self._session.execute(select(ModuleSettings.module_id).
                                             where(ModuleSettings.module_name == module_name))
        return bool(record.scalar())

    async def update_config_by_key(self, module_name: str, module_config:dict, is_active: bool=False):
        record: ModuleSettings = await self._session.execute(select(ModuleSettings).
                                                             where(ModuleSettings.module_name == module_name))
        record.is_active = is_active
        record = record.scalar()
        for key, value in module_config.items():
            record.config[key] = value
        await self._session.commit()
        return record

    async def update_module_is_active(self, module_name: str, is_active: bool):
        await self._session.execute(update(ModuleSettings).
                                    where(ModuleSettings.module_name==module_name).
                                    values(is_active=is_active))
        await self._session.commit()

    async def module_is_active(self, module_name: str):
        check = await self._session.execute(select(ModuleSettings.is_active).
                                    where(ModuleSettings.module_name == module_name))
        return check.scalar()

    async def increment_current_code(self):
        record:ModuleSettings = await self._session.execute(select(ModuleSettings).
                                                            where(ModuleSettings.module_name == Extension.lottery.name))
        record = record.scalar()
        record.config["current_code"] += 1
        await self._session.commit()
        return record









