from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.methods.get_chat import GetChat
from aiogram.methods.kick_chat_member import KickChatMember
from aiogram.dispatcher.fsm.context import FSMContext

from bot.filters.user_status import StatusUserFilter, BotStatusFilter

from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.services.repo.member_repo import MemberRepo

from bot.keyboards.admin_key import generate_admin_key, generate_change_key

from magic_filter import F


from bot.config_reader import config
from bot.templates.text import admin_text


admin_panel_router = Router()
admin_panel_router.message.bind_filter(BotStatusFilter)
admin_panel_router.message.bind_filter(StatusUserFilter)
admin_panel_router.callback_query.bind_filter(BotStatusFilter)
admin_panel_router.callback_query.bind_filter(StatusUserFilter)


@admin_panel_router.message(commands="start", bot_added=True, status_user=["creator", "administrator"])
async def send_mail_panel(message: types.Message):
    chat = await GetChat(chat_id=config.channel_id)
    await message.answer(text=await admin_text.start_message(message.from_user.username, chat.title),
                         reply_markup=await generate_admin_key())

@admin_panel_router.message(commands="start", bot_added=False)
async def bot_not_chat_member(message: types.Message):
    """Бот не является администратором канала/не добавлен в канал"""
    await message.answer(admin_text.BOT_IS_NOT_ADMIN)


@admin_panel_router.callback_query(F.data == "admin_main_panel")
async def main_panel(callback: types.CallbackQuery):
    chat = await GetChat(chat_id=config.channel_id)
    await callback.message.answer(text=await admin_text.start_message(callback.message.from_user.username, chat.title),
                         reply_markup=await generate_admin_key())



