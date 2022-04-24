from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def generate_phone_key():
    phone = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поделиться моим контактом", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True)

    return phone

async def generate_invite_link_key(invite_link):
    keyboard_admin = InlineKeyboardBuilder()
    keyboard_admin.add(
        InlineKeyboardButton(text="Присоедениться в канал", url=invite_link),
    )

    keyboard_admin.adjust(2, 1, repeat=True)
    return keyboard_admin.as_markup()