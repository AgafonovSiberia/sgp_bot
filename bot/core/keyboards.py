from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.dispatcher.filters.callback_data import CallbackData
from bot.config_reader import config


async def generate_admin_key():
    admin_keyboard = InlineKeyboardBuilder()
    admin_keyboard.add(
        InlineKeyboardButton(text="Все подписчики", url=config.GSAPI_URL),
        InlineKeyboardButton(text="\U0001F4DB Забанить пользователя", callback_data="kicked_member"),
        InlineKeyboardButton(text="\U0001F539 Управление поздравлениями", callback_data="anniversary"),
        InlineKeyboardButton(text="\U0001F538 Управление розыгрышем", callback_data="lottery")
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

from bot.service.repo.base import SQLAlchemyRepo
from bot.service.repo.ext import SettingsRepo
from bot.misc.states import Extension

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def user_main_keyboard(chat_link: str, repo: SQLAlchemyRepo):
    lottery_is_active = await repo.get_repo(SettingsRepo).module_is_active(Extension.lottery.name)

    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Перейти в канал", url=chat_link))

    if lottery_is_active:
        keyboard.add(
            InlineKeyboardButton(text="Розыгрыш", callback_data="lottery_to_user"))
    keyboard.adjust(1, 1)
    return keyboard.as_markup()


