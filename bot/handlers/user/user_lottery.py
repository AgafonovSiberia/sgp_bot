from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.fsm.context import FSMContext

from bot.handlers.user import user_panel_router
from bot.keyboards.user_key import user_lottery_keyboard
from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.services.repo.settings_repo import SettingsRepo
from bot.services.repo.lottery_repo import LotteryRepo
from bot.services.repo.member_repo import MemberRepo
from bot.db.models import ChannelMember

from bot.db.models import ModuleSettings, LotteryList
from magic_filter import F

from bot.models.states import Extension
from bot.filters import StatusUserFilter, LotteryActiveFilter, UserInvolvedLotteryFilter
from bot.services.workers.lottery_tasks import generate_lottery_ticket

from bot.services.workers.gsheets_tasks import add_record_in_lottery_list
from bot.templates.text.lottery_text import LOTTERY_CAPTION

user_lottery_router = Router()
user_lottery_router.callback_query.bind_filter(StatusUserFilter)
user_lottery_router.callback_query.bind_filter(LotteryActiveFilter)
user_lottery_router.callback_query.bind_filter(UserInvolvedLotteryFilter)


@user_lottery_router.callback_query(F.data=="lottery_to_user")
async def lottery_main_to_user(callback: types.CallbackQuery):
    await callback.message.answer(text=LOTTERY_CAPTION, reply_markup=await user_lottery_keyboard())


@user_lottery_router.callback_query(F.data == "get_my_code", lottery_is_active=True,
                                    user_is_involved=False)
async def lottery_get_ticket(callback: types.CallbackQuery,  repo: SQLAlchemyRepo):
    """
    Нажатие пользователем кнопки МОЙ КОД
    Лотерея активирована администратором, пользователь ещё не получал билет.
    """
    data: ModuleSettings = await repo.get_repo(SettingsRepo).increment_current_code()
    current_code = data.config.get("current_code")

    await repo.get_repo(LotteryRepo).add_user_ticket(user_id=callback.from_user.id, code=current_code)
    user: ChannelMember = await repo.get_repo(MemberRepo).get_member(user_id=callback.from_user.id)
    add_record_in_lottery_list.delay(user=user, code=current_code)
    #celery task - generate_lottery_ticket
    file_id = generate_lottery_ticket.delay(data_config=data.config, user_id=callback.from_user.id).get()

    await repo.get_repo(LotteryRepo).update_ticket_file_id(user_id=callback.from_user.id, file_id=file_id)

    await callback.answer()



@user_lottery_router.callback_query(F.data == "get_my_code", lottery_is_active=True,
                                    user_is_involved=True)
async def lottery_get_ticket(callback: types.CallbackQuery,  repo: SQLAlchemyRepo, bot: Bot, state:FSMContext):
    """
    Нажатие пользователем кнопки МОЙ КОД
    Лотерея активирована администратором, пользователь уже участвует в розыгрыше и получил билет ранее.
    """
    data: ModuleSettings = await repo.get_repo(SettingsRepo).get_module_settings(Extension.lottery.name)
    ticket_file_id = await repo.get_repo(LotteryRepo).get_ticket_file_id(user_id=callback.from_user.id)
    await callback.message.answer_photo(photo=ticket_file_id, caption=data.config.get('caption'))
    await callback.answer()

