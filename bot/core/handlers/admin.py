from aiogram.methods.get_chat import GetChat
from aiogram import types, loggers
from magic_filter import F

from aiogram.dispatcher.router import Router
from aiogram.methods.kick_chat_member import KickChatMember
from aiogram.dispatcher.fsm.context import FSMContext

from bot.service.repo.base import SQLAlchemyRepo
from bot.service.repo import MemberRepo

from bot.core.filters import UserStatusFilter
from bot.core.keyboards import generate_admin_key, generate_change_key

from bot.misc.states import LeaveMember

from bot.utils.model_converter import channel_member_model_to_member_pydantic
from bot.utils import validators
from bot.templates.text import to_admin

from bot.config_reader import config

admin_router = Router()
admin_router.message.bind_filter(UserStatusFilter)
admin_router.callback_query.bind_filter(UserStatusFilter)


admin_router.message.filter(user_status=["administrator", "creator", "owner"])
admin_router.callback_query.filter(user_status=["administrator", "creator", "owner"])

@admin_router.message(commands="start")
async def send_mail_panel(message: types.Message):
    chat = await GetChat(chat_id=config.channel_id)
    await message.answer(text=await to_admin.start_message(message.from_user.username, chat.title),
                         reply_markup=await generate_admin_key())

@admin_router.callback_query(F.data == "admin_main_panel")
async def main_panel(callback: types.CallbackQuery):
    chat = await GetChat(chat_id=config.channel_id)
    await callback.message.answer(text=await to_admin.start_message(callback.message.from_user.username, chat.title),
                         reply_markup=await generate_admin_key())


@admin_router.callback_query(F.data == "kicked_member")
async def command_banned_member_channel(callback: types.CallbackQuery, state=FSMContext):
    await callback.answer()
    await callback.message.answer(text=to_admin.BANNED_USER)
    await state.set_state(LeaveMember.get_id_member)


@admin_router.message(state=LeaveMember.get_id_member)
async def check_banned_member_channel(message: types.Message, repo: SQLAlchemyRepo, state=FSMContext):
    valid = await validators.validator_is_id(message.text)
    if not valid.is_valid:
        await message.answer(text=await to_admin.not_is_id(valid))
        return

    try:
        member = await repo.get_repo(MemberRepo).get_member(user_id=int(message.text))
        member_pydantic = await channel_member_model_to_member_pydantic(member)
        await message.answer(
            text=await to_admin.profile_text(member_pydantic) + '\n\nВы подтверждаете удаление?',
            reply_markup=await generate_change_key())
        await state.set_state(LeaveMember.check_banned_member)
        await state.update_data(member_data=member_pydantic)
    except Exception as e:
        loggers.event.info(f"Exception: {str(e)}")

        await message.answer("Member not found\n\nПроверьте <b>USER_ID</b> и попробуйте ввести его ещё раз:")


@admin_router.callback_query(F.data == "yes", state=LeaveMember.check_banned_member)
async def banned_member_channel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    member = data["member_data"]
    try:
        result = await KickChatMember(chat_id=config.channel_id, user_id=member.user.user_id)
        if result:
            await callback.message.answer(text=f"Пользователь {member.user.user_name} заблокирован",
                                          disable_notification=True)
            await callback.message.delete()
            await state.clear()
    except Exception as e:
        loggers.event.info(f"Exception: {str(e)}")
        callback.answer(text=f"Не удалось заблокировать пользователя. Text error: {str(e)}")


@admin_router.callback_query(F.data == "no", state=LeaveMember.check_banned_member)
async def not_banned_member_channel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.clear()
    await main_panel(callback.message)
