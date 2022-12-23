from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def user_main_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="МОЙ КОД", callback_data="get_my_code")
    )

    keyboard.adjust(2, 1, repeat=True)
    return keyboard.as_markup()