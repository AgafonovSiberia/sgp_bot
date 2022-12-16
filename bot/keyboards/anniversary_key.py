from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.dispatcher.filters.callback_data import CallbackData
from bot.config_reader import config


class AnniversaryYearCallback(CallbackData, prefix="anniversary_year"):
    year: int

class AnniversaryEditCallback(CallbackData, prefix="anniversary_edit"):
    data_type: str
    year: int


async def anniversary_years_key():
    anniversary_years_keyboard = InlineKeyboardBuilder()
    for current_year in range(1, 26):
        anniversary_years_keyboard.add(
        InlineKeyboardButton(text=current_year,
                             callback_data=AnniversaryYearCallback(year=current_year).pack())
        )

    anniversary_years_keyboard.add(
        InlineKeyboardButton(text="В меню", callback_data="main_panel")
    )
    anniversary_years_keyboard.adjust(5, 5, 5, 5, 5)
    return anniversary_years_keyboard.as_markup()

async def anniversary_edit_params_key(year: int):
    anniversary_edit_params_keyboard = InlineKeyboardBuilder()
    anniversary_edit_params_keyboard.add(
        InlineKeyboardButton(text="Изменить изображение", callback_data=AnniversaryEditCallback(year=year, data_type="img").pack()),
        InlineKeyboardButton(text="Изменить текст", callback_data=AnniversaryEditCallback(year=year, data_type="text").pack()),
        InlineKeyboardButton(text="В меню", callback_data="congratulation")
    )
    anniversary_edit_params_keyboard.adjust(2)
    return anniversary_edit_params_keyboard.as_markup()

async def anniversary_menu_key():
    anniversary_menu_keyboard = InlineKeyboardBuilder()
    anniversary_menu_keyboard.add(
        InlineKeyboardButton(text="В меню", callback_data="congratulation")
    )


