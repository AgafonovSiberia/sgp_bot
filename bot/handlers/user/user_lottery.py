from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.fsm.context import FSMContext
from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.services.repo.settings_repo import SettingsRepo
from bot.services.repo.lottery_repo import LotteryRepo

from bot.db.models import ModuleSettings, LotteryList
from magic_filter import F

from bot.models.states import Extension
from bot.filters import StatusUserFilter, LotteryActiveFilter, UserInvolvedLotteryFilter
from bot.services.workers.lottery_tasks import generate_lottery_ticket

from bot.services.workers.gsheets_tasks import add_record_in_lottery_list

user_lottery_router = Router()
user_lottery_router.callback_query.bind_filter(StatusUserFilter)
user_lottery_router.callback_query.bind_filter(LotteryActiveFilter)
user_lottery_router.callback_query.bind_filter(UserInvolvedLotteryFilter)


@user_lottery_router.callback_query(F.data == "get_my_code", lottery_is_active=True,
                                    user_is_involved=False)
async def lottery_get_ticket(callback: types.CallbackQuery,  repo: SQLAlchemyRepo):
    data: ModuleSettings = await repo.get_repo(SettingsRepo).increment_current_code()
    current_code = data.config.get("current_code")
    await repo.get_repo(LotteryRepo).add_user_ticket(user_id=callback.from_user.id, code=current_code)
    add_record_in_lottery_list.delay(user_id=callback.message.from_user.id,code=current_code,
                                    username=callback.message.from_user.username)

    file_id = generate_lottery_ticket.delay(data_config=data.config, user_id=callback.from_user.id).get()

    await repo.get_repo(LotteryRepo).update_ticket_file_id(user_id=callback.from_user.id, file_id=file_id)

    await callback.answer()



@user_lottery_router.callback_query(F.data == "get_my_code", lottery_is_active=True,
                                    user_is_involved=True)
async def lottery_get_ticket(callback: types.CallbackQuery,  repo: SQLAlchemyRepo, bot: Bot, state:FSMContext):
    await callback.answer()
    data: ModuleSettings = await repo.get_repo(SettingsRepo).get_module_settings(Extension.lottery.name)
    ticket_file_id = await repo.get_repo(LotteryRepo).get_ticket_file_id(user_id=callback.message.from_user.id)
    await callback.message.answer_photo(photo=ticket_file_id, caption=data.config.get('caption'))











