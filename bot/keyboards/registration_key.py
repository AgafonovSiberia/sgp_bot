from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def generate_phone_key():
    keyboard_phone = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поделиться моим контактом", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard_phone

async def generate_invite_link_key(invite_link):
    keyboard_link = InlineKeyboardBuilder()
    keyboard_link.add(
        InlineKeyboardButton(text="Присоединиться в канал", url=invite_link),
    )

    keyboard_link.adjust(2, 1, repeat=True)
    return keyboard_link.as_markup()