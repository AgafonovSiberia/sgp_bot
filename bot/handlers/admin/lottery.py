from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.fsm.context import FSMContext
from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.services.repo.settings_repo import SettingsRepo
from bot.db.models import ModuleSettings
from aiogram.types import ContentType
from aiogram.dispatcher.filters import ContentTypesFilter
from bot.models.states import GetCongratulateData
from magic_filter import F

from bot.filters.ext import LotteryTicketTemplateStateFilter
from bot.filters import SlotStateFilter
from bot.models.states import SlotStates, Extension
from bot.templates.text import lottery_text
from aiogram import loggers


from bot.keyboards.lottery_key import lottery_keyboard, LotteryCallback, ticket_update_keyboard
from bot.models.states import LotteryTemplate

admin_lottery_router = Router()
admin_lottery_router.callback_query.bind_filter(LotteryTicketTemplateStateFilter)


async def set_primary_module_settings(repo: SQLAlchemyRepo):
    check_lottery = await repo.get_repo(SettingsRepo).check_modules_settings(module_name="lottery")
    if not check_lottery:
        await repo.get_repo(SettingsRepo).add_module_settings(module_name=Extension.lottery.name,
                                                              is_active=False,
                                                              module_config={"template_id": None,
                                                                             "caption": None,
                                                                             "current_code": 0})

@admin_lottery_router.callback_query(F.data == "lottery")
async def lottery_main(callback: types.CallbackQuery, repo: SQLAlchemyRepo, state=FSMContext ):
    await callback.answer()
    await set_primary_module_settings(repo=repo)

    settings: ModuleSettings = await repo.get_repo(SettingsRepo).get_module_settings(module_name=Extension.lottery.name)

    await callback.message.answer(text=lottery_text.LOTTERY_PANEL,
                                  reply_markup=await lottery_keyboard(lottery_is_active=settings.is_active,
                                                                      template_is_full=settings.config.get("template_id") is not None))


@admin_lottery_router.callback_query(LotteryCallback.filter())
async def lottery_activated(callback: types.CallbackQuery, callback_data: LotteryCallback,
                            repo: SQLAlchemyRepo):
    await callback.answer()
    await repo.get_repo(SettingsRepo).update_module_is_active(module_name=Extension.lottery.name,
                                                              is_active=callback_data.is_active)
    await callback.message.edit_reply_markup(
        reply_markup=await lottery_keyboard(lottery_is_active=callback_data.is_active))

@admin_lottery_router.callback_query(F.data == "ticket_template", ticket_template_state=SlotStates.IS_FULL)
async def update_ticket_template(callback: types.CallbackQuery, state: FSMContext, repo: SQLAlchemyRepo):
    loggers.event.info(
        f"Custom log - module:{__name__} - {callback.from_user.username}:{callback.from_user.id} - запросил изменение шаблона")
    await callback.message.delete()
    settings: ModuleSettings = await repo.get_repo(SettingsRepo).get_module_settings(module_name=Extension.lottery.name)
    await callback.answer()
    await callback.message.answer_photo(photo=settings.config.get("template_id"), caption=settings.config.get("caption"),
                                  reply_markup=await ticket_update_keyboard(template_state=SlotStates.IS_FULL))


@admin_lottery_router.callback_query(F.data == "ticket_template", ticket_template_state = SlotStates.IS_EMPTY)
async def update_ticket_template(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer(text=lottery_text.TEMPLATE_TICKET_NOT_FOUND,
                                  reply_markup=await ticket_update_keyboard(template_state=SlotStates.IS_EMPTY))


@admin_lottery_router.callback_query(F.data == "update_ticket_template")
async def update_ticket_template(callback: types.CallbackQuery, state:FSMContext):
    loggers.event.info(
        f"Custom log - module:{__name__} - {callback.from_user.username}:{callback.from_user.id} - запросил изменение шаблона")
    await callback.message.delete()
    await callback.answer()
    await state.set_state(LotteryTemplate.template)
    await callback.message.answer(text=lottery_text.GET_TEMPLATE_TICKET)

@admin_lottery_router.message(state=LotteryTemplate.template, content_types=[ContentType.PHOTO], )
async def get_ticket_template(message: types.Message, repo: SQLAlchemyRepo, state: FSMContext):
    loggers.event.info(
        f"Custom log - module:{__name__} - {message.from_user.id}:{message.from_user.username} - загрузил новый шаблон")
    settings: ModuleSettings = await repo.get_repo(SettingsRepo).update_config_by_key(module_name=Extension.lottery.name,
                                                                                      data={"template_id":message.photo[-1].file_id,
                                                                 "caption":message.caption})
    await state.clear()

    await message.answer(text=lottery_text.LOTTERY_PANEL,
                                  reply_markup=await lottery_keyboard(lottery_is_active=settings.is_active,
                                                                      template_is_full=settings.config.get(
                                                                          "template_id") is not None))












