from aiogram import types
from aiogram.dispatcher.filters import BaseFilter

from bot.misc.states import SlotStates, Extension
from bot.database.models import ModuleSettings
from bot.service.repo.base import SQLAlchemyRepo
from bot.database.models import CongratulationData
from bot.service.repo.ext import SettingsRepo, LotteryRepo, AnniversaryRepo


class SlotStateFilter(BaseFilter):
    """Заполнен ли слот с открыткой"""
    slot_state: SlotStates
    async def __call__(self, callback: types.CallbackQuery, repo: SQLAlchemyRepo) -> bool:
        if callback.data:
            year = callback.data.split(sep=":")[1]
            data: CongratulationData = await repo.get_repo(AnniversaryRepo).get_congratulation_data(
                slot_id=int(year))
        current_state = SlotStates.IS_EMPTY
        if data:
            current_state = SlotStates.IS_FULL
        return current_state == self.slot_state