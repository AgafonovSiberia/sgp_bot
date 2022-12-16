from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.dispatcher.filters.callback_data import CallbackData
from bot.config_reader import config


async def generate_admin_key():
    admin_keyboard = InlineKeyboardBuilder()
    admin_keyboard.add(
        InlineKeyboardButton(text="Все подписчики", url=config.GSAPI_URL),
        InlineKeyboardButton(text="Забанить", callback_data="kicked_member"),
        InlineKeyboardButton(text="Поздравления", callback_data="congratulation")
    )

    admin_keyboard.adjust(2, 1, repeat=True)
    return admin_keyboard.as_markup()





async def generate_change_key():
    admin_keyboard = InlineKeyboardBuilder()
    admin_keyboard.add(
        InlineKeyboardButton(text="Подтверждаю", callback_data="yes"),
        InlineKeyboardButton(text="Отмена", callback_data="no")
    )
    admin_keyboard.adjust(2, repeat=True)
    return admin_keyboard.as_markup()
