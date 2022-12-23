from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.methods.get_chat import GetChat
from aiogram.methods.kick_chat_member import KickChatMember
from aiogram.dispatcher.fsm.context import FSMContext

from bot.filters.user_status import StatusUserFilter, BotStatusFilter
from bot.filters import LotteryActiveFilter
from bot.templates.text.lottery_text import LOTTERY_CAPTION
from bot.templates.text.exceptions_text import status_is_member

from bot.filters import UserIsUnknownFilter
from bot.keyboards.user_key import user_main_keyboard

user_panel_router = Router()
user_panel_router.message.bind_filter(UserIsUnknownFilter)
user_panel_router.message.bind_filter(BotStatusFilter)
user_panel_router.message.bind_filter(StatusUserFilter)
user_panel_router.message.bind_filter(LotteryActiveFilter)

@user_panel_router.message(commands="start", bot_added=True, status_user="member",
                                   user_is_known=True, lottery_is_active=True)
async def user_status_is_member(message: types.Message):
    """Пользователь уже подписан на канал и прошёл регистрацию через бота"""
    await message.answer(text=LOTTERY_CAPTION, reply_markup=await user_main_keyboard())


@user_panel_router.message(commands="start", bot_added=True, status_user="member",
                                   user_is_known=True, lottery_is_active=False)
async def user_main(message: types.Message):
    await message.answer(text=await status_is_member(username=message.from_user.username))




