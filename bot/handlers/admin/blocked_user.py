from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.methods.get_chat import GetChat
from aiogram.methods.kick_chat_member import KickChatMember
from aiogram.dispatcher.fsm.context import FSMContext


from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.services.repo.member_repo import MemberRepo

from bot.keyboards.admin_key import generate_admin_key, generate_change_key

from magic_filter import F
from bot.models.states import LeaveMember

from bot.utils.to_pydantic import channel_member_model_to_member_pydantic
from bot.utils import validators
from aiogram import loggers

from bot.config_reader import config
from bot.templates.text import admin_text

from .admin_panel import main_panel

blocked_user_router = Router()


@blocked_user_router.callback_query(F.data == "kicked_member")
async def command_banned_member_channel(callback: types.CallbackQuery, state=FSMContext):
    await callback.answer()
    await callback.message.answer(text=admin_text.BANNED_USER)
    await state.set_state(LeaveMember.get_id_member)


@blocked_user_router.message(state=LeaveMember.get_id_member)
async def check_banned_member_channel(message: types.Message, repo: SQLAlchemyRepo, state=FSMContext):
    valid = await validators.validator_is_id(message.text)
    if not valid.is_valid:
        await message.answer(text=await admin_text.not_is_id(valid))
        return

    try:
        member = await repo.get_repo(MemberRepo).get_member(user_id=int(message.text))
        member_pydantic = await channel_member_model_to_member_pydantic(member)
        await message.answer(
            text=await admin_text.profile_text(member_pydantic) + '\n\nВы подтверждаете удаление?',
            reply_markup=await generate_change_key())
        await state.set_state(LeaveMember.check_banned_member)
        await state.update_data(member_data=member_pydantic)
    except Exception as e:
        loggers.event.info(
            f"Custom log - module:{__name__} - Exception: {str(e)}")

        await message.answer("Member not found\n\nПроверьте <b>USER_ID</b> и попробуйте ввести его ещё раз:")


@blocked_user_router.callback_query(F.data == "yes", state=LeaveMember.check_banned_member)
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
        loggers.event.info(
            f"Custom log - module:{__name__} - Exception: {str(e)}")
        callback.answer(text=f"Не удалось заблокировать пользователя. Text error: {str(e)}")


@blocked_user_router.callback_query(F.data == "no", state=LeaveMember.check_banned_member)
async def not_banned_member_channel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.clear()
    await main_panel(callback.message)
