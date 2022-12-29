from bot.services.repo.base import SQLAlchemyRepo
from bot.services.repo.ext import SettingsRepo
from bot.models.states import Extension

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

async def user_lottery_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="МОЙ КОД", callback_data="get_my_code")
    )

    keyboard.adjust(2, 1, repeat=True)
    return keyboard.as_markup()

