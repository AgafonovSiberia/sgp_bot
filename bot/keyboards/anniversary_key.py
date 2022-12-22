from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.dispatcher.filters.callback_data import CallbackData
from bot.filters.slot_state import SlotStates


class AnniversaryYearCallback(CallbackData, prefix="anniversary_year"):
    slot_id: int


class SlotUpdateCallback(CallbackData, prefix="anniversary_edit"):
    slot_id: int


async def anniversary_years_key():
    anniversary_years_keyboard = InlineKeyboardBuilder()
    for current_slot in range(1, 26):
        anniversary_years_keyboard.add(
        InlineKeyboardButton(text=current_slot,
                             callback_data=AnniversaryYearCallback(slot_id=current_slot).pack())
        )

    anniversary_years_keyboard.add(
        InlineKeyboardButton(text="В главное меню", callback_data="admin_main_panel")
    )
    anniversary_years_keyboard.adjust(5, 5, 5, 5, 5)
    return anniversary_years_keyboard.as_markup()


async def update_slot_keyboard(slot_id: int, current_slot_state: SlotStates):
    edit_slots_keyboard = InlineKeyboardBuilder()

    if current_slot_state == SlotStates.IS_EMPTY:
        edit_slots_keyboard.add(
            InlineKeyboardButton(text="Добавить открытку", callback_data=SlotUpdateCallback(slot_id=slot_id).pack()))

    elif current_slot_state == SlotStates.IS_FULL:
        edit_slots_keyboard.add(InlineKeyboardButton(text="Заменить открытку", callback_data=SlotUpdateCallback(slot_id=slot_id).pack()))


    edit_slots_keyboard.add(
        InlineKeyboardButton(text="Назад", callback_data="congratulation")
    )
    edit_slots_keyboard.adjust(1, 1)
    return edit_slots_keyboard.as_markup()

async def anniversary_menu_key():
    anniversary_menu_keyboard = InlineKeyboardBuilder()
    anniversary_menu_keyboard.add(
        InlineKeyboardButton(text="Назад", callback_data="congratulation")
    )


