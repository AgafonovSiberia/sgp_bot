from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters.callback_data import CallbackData

from bot.models.states import SlotStates


class AnniversaryYearCallback(CallbackData, prefix="anniversary_year"):
    slot_id: int


class SlotUpdateCallback(CallbackData, prefix="anniversary_edit"):
    slot_id: int


class AnniversaryCallback(CallbackData, prefix="anniversary_callback"):
    is_active: bool

async def anniversary_key(anniversary_is_active: bool):
    """
    Панель "Управление поздравлениями"
    :param anniversary_is_active: текущее состояние рассылки подздравлений (активирована/остановлена)
    :return: keyboard for message.reply_markup
    """
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="\U000023F9 Остановить рассылку" if anniversary_is_active else "\U000025B6	Активировать рассылку",
            callback_data=AnniversaryCallback(is_active=not anniversary_is_active).pack()),

        InlineKeyboardButton(
            text="\U0001F4DD Редактировать открытки",
            callback_data="edit_anniversary_slots"),

        InlineKeyboardButton(
            text="\U0001F501 Синхронизировать даты",
            callback_data="sync_employment_date"
        ),

        InlineKeyboardButton(
            text="\U000021A9 В главное меню",
            callback_data="admin_main_panel")
    )

    keyboard.adjust(2, 1)
    return keyboard.as_markup()




async def anniversary_slots_key():
    """
    Слоты для открыток от 1 до 25 (соответствуют годам)
    :return: keyboard for message.reply_markup
    """
    anniversary_years_keyboard = InlineKeyboardBuilder()
    for current_slot in range(1, 26):
        anniversary_years_keyboard.add(
        InlineKeyboardButton(text=current_slot,
                             callback_data=AnniversaryYearCallback(slot_id=current_slot).pack())
        )
    anniversary_years_keyboard.add(
        InlineKeyboardButton(text="\U000021A9 В меню", callback_data="anniversary")
    )
    anniversary_years_keyboard.adjust(5, 5, 5, 5, 5)
    return anniversary_years_keyboard.as_markup()


async def update_slot_key(slot_id: int, current_slot_state: SlotStates):
    """
    Панель меню - "редактировать открытки"
    :param slot_id: id-слота с открыткой (соответствует кол-ву лет)
    :param current_slot_state: текущее состояние слота (IS_EMPTY / IS_FULL)
    :return: keyboard for message.reply_markup
    """
    keyboard = InlineKeyboardBuilder()


    keyboard.add(
        InlineKeyboardButton
        (text="\U00002795 Добавить открытку", callback_data=SlotUpdateCallback(slot_id=slot_id).pack())
        if current_slot_state == SlotStates.IS_EMPTY
        else InlineKeyboardButton
        (text="\U0001F504 Заменить открытку", callback_data=SlotUpdateCallback(slot_id=slot_id).pack())
    )

    keyboard.add(
        InlineKeyboardButton(text="\U000021A9 Назад", callback_data="edit_anniversary_slots")
    )
    keyboard.adjust(1, 1)
    return keyboard.as_markup()

