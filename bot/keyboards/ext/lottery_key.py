from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.dispatcher.filters.callback_data import CallbackData
from bot.config_reader import config
from bot.models.states import SlotStates

class LotteryCallback(CallbackData, prefix="lottery_callback"):
    is_active: bool

async def lottery_keyboard(lottery_is_active: bool, template_is_full: bool = True):
    keyboard = InlineKeyboardBuilder()
    if template_is_full:
        keyboard.add(
            InlineKeyboardButton(
                text="\U000023F9 Остановить розыгрыш" if lottery_is_active else "\U000025B6	Активировать розыгрыш",
                callback_data=LotteryCallback(is_active=not lottery_is_active).pack())
        )
    keyboard.add(
        InlineKeyboardButton(
            text="Шаблон билета",
            callback_data = "ticket_template"),
        InlineKeyboardButton(
            text="В главное меню",
            callback_data = "admin_main_panel"
        )
    )
    keyboard.adjust(2, 1)
    return keyboard.as_markup()

async def ticket_update_keyboard(template_state: SlotStates):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Добавить шаблон" if template_state == SlotStates.IS_EMPTY else "Изменить шаблон",
        callback_data = "update_ticket_template"),
        InlineKeyboardButton(
            text="В меню", callback_data="lottery")
    )
    keyboard.adjust(2)
    return keyboard.as_markup()

