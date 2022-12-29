from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.methods.get_chat import GetChat

from bot.filters.user_status import BotStatusFilter

from bot.keyboards.admin_key import generate_admin_key
from bot.templates.text import to_admin

from magic_filter import F


from bot.config_reader import config

admin_panel_router = Router()
admin_panel_router.message.bind_filter(BotStatusFilter)
admin_panel_router.callback_query.bind_filter(BotStatusFilter)



@admin_panel_router.message(commands="start", bot_added=True)
async def send_mail_panel(message: types.Message):
    chat = await GetChat(chat_id=config.channel_id)
    await message.answer(text=await to_admin.start_message(message.from_user.username, chat.title),
                         reply_markup=await generate_admin_key())

@admin_panel_router.message(commands="start", bot_added=False)
async def bot_not_chat_member(message: types.Message):
    """Бот не является администратором канала/не добавлен в канал"""
    await message.answer(to_admin.BOT_IS_NOT_ADMIN)


@admin_panel_router.callback_query(F.data == "admin_main_panel")
async def main_panel(callback: types.CallbackQuery):
    chat = await GetChat(chat_id=config.channel_id)
    await callback.message.answer(text=await to_admin.start_message(callback.message.from_user.username, chat.title),
                         reply_markup=await generate_admin_key())



