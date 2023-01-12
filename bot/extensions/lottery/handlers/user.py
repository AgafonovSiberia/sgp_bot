from magic_filter import F

from aiogram import types
from aiogram.dispatcher.router import Router

from bot.db.models import ChannelMember, ModuleSettings
from bot.templates.text.ext.to_lottery import LOTTERY_CAPTION
from bot.filters import StatusUserFilter, LotteryActiveFilter, UserInvolvedLotteryFilter
from bot.models.states import Extension

from bot.keyboards.user_key import user_lottery_keyboard

from bot.services.repo import MemberRepo
from bot.services.repo.base import SQLAlchemyRepo
from bot.services.repo.ext import SettingsRepo, LotteryRepo


from bot.services.workers.tasks.ext import generate_lottery_ticket
from bot.services.workers.tasks import add_record_in_lottery_list


user_lottery_router = Router()
user_lottery_router.callback_query.bind_filter(StatusUserFilter)
user_lottery_router.callback_query.bind_filter(LotteryActiveFilter)
user_lottery_router.callback_query.bind_filter(UserInvolvedLotteryFilter)


@user_lottery_router.callback_query(F.data=="lottery_to_user")
async def lottery_main_to_user(callback: types.CallbackQuery):
    """
    User click to button "Розыгрыш"
    """
    await callback.message.answer(text=LOTTERY_CAPTION, reply_markup=await user_lottery_keyboard())


@user_lottery_router.callback_query(F.data == "get_my_code",
                                    lottery_is_active=True, user_is_involved=False)
async def lottery_get_ticket(callback: types.CallbackQuery,  repo: SQLAlchemyRepo):
    """
    User click to button "Мой код"
    Filters_states: lottery is active, user is not involved
    :param callback:
    :param repo:
    :return:
    """

    await callback.message.delete()
    data: ModuleSettings = await repo.get_repo(SettingsRepo).increment_current_code()
    current_code = data.config.get("current_code")

    await repo.get_repo(LotteryRepo).add_user_ticket(user_id=callback.from_user.id, code=current_code)
    user: ChannelMember = await repo.get_repo(MemberRepo).get_member(user_id=callback.from_user.id)

    #celery tasks
    add_record_in_lottery_list.delay(user=user, code=current_code)
    file_id = generate_lottery_ticket.delay(data_config=data.config, user_id=callback.from_user.id).get()

    await repo.get_repo(LotteryRepo).update_ticket_file_id(user_id=callback.from_user.id, file_id=file_id)
    await callback.answer()



@user_lottery_router.callback_query(F.data == "get_my_code",
                                    lottery_is_active=True, user_is_involved=True)
async def lottery_get_ticket(callback: types.CallbackQuery,  repo: SQLAlchemyRepo):
    """
    User click to button "Мой код"
    Filters_states: lottery is active, user is involved
    :param callback:
    :param repo:
    :return:
    """
    await callback.message.delete()

    data: ModuleSettings = await repo.get_repo(SettingsRepo).get_module_settings(Extension.lottery.name)
    ticket_file_id = await repo.get_repo(LotteryRepo).get_ticket_file_id(user_id=callback.from_user.id)

    await callback.message.answer_photo(photo=ticket_file_id, caption=data.config.get('caption'))
    await callback.answer()

