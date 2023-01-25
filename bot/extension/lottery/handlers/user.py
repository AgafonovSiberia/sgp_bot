from magic_filter import F

from aiogram import types
from aiogram.dispatcher.router import Router

from bot.database.models import ChannelMember, ModuleSettings, Lottery
from bot.templates.text.ext.to_lottery import LOTTERY_CAPTION
from bot.extension.lottery.filters import LotteryActiveFilter, UserInvolvedLotteryFilter


from bot.misc.states import Extension

from bot.extension.lottery.keyboards import user_lottery_keyboard

from bot.service.repo import MemberRepo
from bot.service.repo.base import SQLAlchemyRepo
from bot.service.repo.ext import SettingsRepo, LotteryRepo


from bot.service.workflow.tasks.ext.lottery_tasks import generate_lottery_ticket
from bot.service.workflow.tasks import add_record_in_lottery_list


user_lottery_router = Router()
user_lottery_router.callback_query.bind_filter(LotteryActiveFilter)
user_lottery_router.callback_query.bind_filter(UserInvolvedLotteryFilter)


@user_lottery_router.callback_query(F.data=="lottery_to_user")
async def lottery_main_to_user(callback: types.CallbackQuery):
    """
    User click to button "Розыгрыш"
    """
    await callback.answer()
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


    lottery_record:Lottery = await repo.get_repo(LotteryRepo).add_user_ticket(user_id=callback.from_user.id)
    data: ModuleSettings = await repo.get_repo(SettingsRepo).get_module_settings(Extension.lottery.name)

    data.config["current_code"] = lottery_record.code

    user: ChannelMember = await repo.get_repo(MemberRepo).get_member(user_id=lottery_record.user_id)


    add_record_in_lottery_list.delay(user=user, code=lottery_record.code)
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

