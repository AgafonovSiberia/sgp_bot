from aiogram import types
from aiogram.dispatcher.filters import BaseFilter

from bot.misc.states import SlotStates, Extension
from bot.database.models import ModuleSettings
from bot.service.repo.base import SQLAlchemyRepo
from bot.service.repo.ext import SettingsRepo, LotteryRepo


class LotteryActiveFilter(BaseFilter):
    """Проверка на то, активирован ли розыгрыш администором"""
    lottery_is_active: bool
    async def __call__(self, callback: types.CallbackQuery, repo: SQLAlchemyRepo) -> bool:
        current_state: ModuleSettings = await repo.get_repo(SettingsRepo).\
            module_is_active(module_name=Extension.lottery.name)
        return current_state == self.lottery_is_active


class LotteryTicketTemplateStateFilter(BaseFilter):
    ticket_template_state: SlotStates
    async def __call__(self, callback: types.CallbackQuery, repo: SQLAlchemyRepo) -> bool:
        settings: ModuleSettings = await repo.get_repo(SettingsRepo).\
            get_module_settings(module_name=Extension.lottery.name)
        current_state = SlotStates.IS_EMPTY
        if settings and settings.config.get("template_id"):
            current_state = SlotStates.IS_FULL
        return current_state == self.ticket_template_state

class UserInvolvedLotteryFilter(BaseFilter):
    """Пользователь уже участвует в розыгрыше"""
    user_is_involved: bool

    async def __call__(self, callback:types.CallbackQuery, repo:SQLAlchemyRepo) -> bool:
        check_user = await repo.get_repo(LotteryRepo).check_user_in_lottery(user_id=callback.from_user.id)
        return check_user == self.user_is_involved