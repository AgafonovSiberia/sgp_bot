from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.methods.get_chat import GetChat
from aiogram.methods.kick_chat_member import KickChatMember
from aiogram.dispatcher.fsm.context import FSMContext

from bot.filters.user_status import StatusUserFilter, BotStatusFilter

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

from bot.filters import UserIsUnknownFilter
from bot.keyboards.user_key import user_main_keyboard

user_panel_router = Router()
user_panel_router.message.bind_filter(UserIsUnknownFilter)
user_panel_router.message.bind_filter(BotStatusFilter)
user_panel_router.message.bind_filter(StatusUserFilter)


@user_panel_router.message(commands="start", bot_added=True, status_user="member",
                                   user_is_known=True)
async def user_status_is_member(message: types.Message, state: FSMContext, bot: Bot):
    """Пользователь уже подписан на канал и прошёл регистрацию через бота"""
    await message.answer(text="Братан, можно поучаствовать в конкурсе", reply_markup=await user_main_keyboard())


