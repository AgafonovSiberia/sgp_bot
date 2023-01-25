from magic_filter import F

from aiogram import types, Bot, Dispatcher
from aiogram.types import ContentType
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.fsm.context import FSMContext

from bot.extension.anniversary.filters import SlotStateFilter
from bot.templates.text.ext import to_anniversary
from bot.misc.states import GetCongratulateData, SlotStates, Extension
from bot.service.repo.base import SQLAlchemyRepo
from bot.service.repo.ext import AnniversaryRepo, SettingsRepo
from bot.utils.fake_updates import create_fake_callback
from bot.database.models import ModuleSettings


from bot.extension.anniversary.keyboards import anniversary_slots_key,update_slot_key,\
    AnniversaryYearCallback, SlotUpdateCallback, anniversary_key, AnniversaryCallback

from bot.service.workflow.tasks.periodic_tasks import sync_date_engine


anniversary_admin_router = Router()
anniversary_admin_router.callback_query.bind_filter(SlotStateFilter)


async def set_primary_module_settings(repo: SQLAlchemyRepo):
    check_lottery = await repo.get_repo(SettingsRepo).check_modules_settings(module_name=Extension.anniversary.name)
    if not check_lottery:
        await repo.get_repo(SettingsRepo).add_module_settings(module_name=Extension.anniversary.name,
                                                              is_active=False,
                                                              module_config={})

@anniversary_admin_router.callback_query(F.data == "anniversary")
async def anniversary_main_panel(callback: types.CallbackQuery, repo: SQLAlchemyRepo):
    await set_primary_module_settings(repo=repo)

    settings: ModuleSettings = await repo.get_repo(SettingsRepo).get_module_settings(module_name=Extension.anniversary.name)

    await callback.message.answer(text=to_anniversary.ANNIVERSARY_PANEL,
                                  reply_markup=await anniversary_key(anniversary_is_active=settings.is_active))
    await callback.answer()

@anniversary_admin_router.callback_query(F.data == "sync_employment_date")
async def sync_employment_date(callback: types.CallbackQuery):
    sync_date_engine.delay()
    await callback.answer()



@anniversary_admin_router.callback_query(AnniversaryCallback.filter())
async def anniversary_activated(callback: types.CallbackQuery, callback_data: AnniversaryCallback,
                            repo: SQLAlchemyRepo):
    await callback.answer()
    await repo.get_repo(SettingsRepo).update_module_is_active(module_name=Extension.anniversary.name,
                                                              is_active=callback_data.is_active)
    await callback.message.edit_reply_markup(
        reply_markup=await anniversary_key(anniversary_is_active=callback_data.is_active))


@anniversary_admin_router.callback_query(F.data == "edit_anniversary_slots")
async def edit_anniversary_slots(callback: types.CallbackQuery, repo: SQLAlchemyRepo):
    await callback.message.answer(text=to_anniversary.ANNIVERSARY_EDIT_SLOTS,
                                  reply_markup=await anniversary_slots_key())
    await callback.answer()


@anniversary_admin_router.callback_query(AnniversaryYearCallback.filter(), slot_state=SlotStates.IS_EMPTY)
async def get_anniversary_year(callback: types.CallbackQuery, callback_data: AnniversaryYearCallback,):
    await callback.answer()
    await callback.message.answer(text=await to_anniversary.slot_is_empty(slot_id=callback_data.slot_id),
                                  reply_markup=await update_slot_key(slot_id=callback_data.slot_id, current_slot_state=SlotStates.IS_EMPTY))



@anniversary_admin_router.callback_query(AnniversaryYearCallback.filter(), slot_state=SlotStates.IS_FULL)
async def get_anniversary_year(callback: types.CallbackQuery, callback_data: AnniversaryYearCallback, repo: SQLAlchemyRepo, bot: Bot, state: FSMContext, ):
    await callback.answer()
    data = await repo.get_repo(AnniversaryRepo).get_congratulation_data(slot_id=callback_data.slot_id)
    await callback.message.answer_photo(photo=data.img_id, caption=data.caption,
                                        reply_markup=await update_slot_key(slot_id=callback_data.slot_id, current_slot_state=SlotStates.IS_FULL))


@anniversary_admin_router.callback_query(SlotUpdateCallback.filter())
async def edit_anniversary_img(callback: types.CallbackQuery, callback_data: AnniversaryYearCallback, repo: SQLAlchemyRepo, bot: Bot, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text=f"Отправьте картинку, в описание вставьте текст поздравления")
    await state.set_state(GetCongratulateData.image)
    await state.update_data(current_slot=callback_data.slot_id)


@anniversary_admin_router.message(state=GetCongratulateData.image, content_types=[ContentType.PHOTO])
async def get_congratulate_text(message: types.Message, repo: SQLAlchemyRepo, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await repo.get_repo(AnniversaryRepo).add_congratulation_data(slot_id=data.get("current_slot"),
                                                                 img_id=message.photo[-1].file_id,
                                                                 caption=message.caption)
    await state.clear()

    await edit_anniversary_slots(callback=await create_fake_callback(fake_user=message.from_user,
                                                                     callback_data="edit_anniversary_slots"), repo=repo)






