from abc import ABC

from aiogram import types
from aiogram.dispatcher.filters import BaseFilter
from bot.services.repo.settings_repo import SettingsRepo
from bot.db.models import ModuleSettings, CongratulationData
from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.services.repo.congratulation_repo import CongratulationRepo
from bot.services.repo.lottery_repo import LotteryRepo
from bot.db.models import CongratulationData
from bot.models.states import SlotStates, Extension



class UserInvolvedLotteryFilter(BaseFilter):
    """Пользователь уже участвует в розыгрыше"""
    user_is_involved: bool

    async def __call__(self, callback:types.CallbackQuery, repo:SQLAlchemyRepo) -> bool:
        check_user = await repo.get_repo(LotteryRepo).check_user_in_lottery(user_id=callback.message.from_user.id)
        return check_user == self.user_is_involved


class LotteryActiveFilter(BaseFilter):
    """Проверка на то, активирован ли розыгрыш администором"""
    lottery_is_active: bool
    async def __call__(self, callback: types.CallbackQuery, repo: SQLAlchemyRepo) -> bool:
        current_state: ModuleSettings = await repo.get_repo(SettingsRepo).get_module_settings(Extension.lottery.name)
        if current_state:
            return current_state.is_active == self.lottery_is_active
        return False == self.lottery_is_active

    


class SlotStateFilter(BaseFilter):
    """Заполнен ли слот с открыткой"""
    slot_state: SlotStates
    async def __call__(self, callback: types.CallbackQuery, repo: SQLAlchemyRepo) -> bool:
        if callback.data:
            print(callback.data)
            year = callback.data.split(sep=":")[1]
            data: CongratulationData = await repo.get_repo(CongratulationRepo).get_congratulation_data(
                slot_id=int(year))
        current_state = SlotStates.IS_EMPTY
        if data:
            current_state = SlotStates.IS_FULL
        return current_state == self.slot_state


class LotteryTicketTemplateStateFilter(BaseFilter):
    ticket_template_state: SlotStates
    async def __call__(self, callback: types.CallbackQuery, repo: SQLAlchemyRepo) -> bool:
        settings: ModuleSettings = await repo.get_repo(SettingsRepo).\
            get_module_settings(module_name=Extension.lottery.name)
        current_state = SlotStates.IS_EMPTY
        if settings and settings.config.get("template_id"):
            current_state = SlotStates.IS_FULL
        return current_state == self.ticket_template_state
