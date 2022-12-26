from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.fsm.context import FSMContext
from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.services.repo.congratulation_repo import CongratulationRepo
from aiogram.types import ContentType
from aiogram.dispatcher.filters import ContentTypesFilter
from bot.models.states import GetCongratulateData
from magic_filter import F

from bot.filters import SlotStateFilter
from bot.models.states import SlotStates

from bot.keyboards.anniversary_key import anniversary_years_key,update_slot_keyboard,\
    AnniversaryYearCallback, SlotUpdateCallback


anniversary_router = Router()
anniversary_router.callback_query.bind_filter(SlotStateFilter)

@anniversary_router.callback_query(F.data == "congratulation")
async def congratulation_params(callback: types.CallbackQuery, state=FSMContext):
    await callback.answer()
    await callback.message.answer(text="Какой год лалал", reply_markup=await anniversary_years_key())


#
# @anniversary_router.callback_query(AnniversaryYearCallback.filter(), slot_state=SlotStates.IS_EMPTY)
# async def get_anniversary_year(callback: types.CallbackQuery, callback_data: AnniversaryYearCallback, repo: SQLAlchemyRepo, bot: Bot, state: FSMContext, ):
#     await callback.answer()
#     await callback.message.answer(text=f"СЛОТ №{callback_data.slot_id}\nВ базе данных отсутствуют данные для выбранного слота",
#                                   reply_markup=await update_slot_keyboard(slot_id=callback_data.slot_id, current_slot_state=SlotStates.IS_EMPTY))
#


# @anniversary_router.callback_query(AnniversaryYearCallback.filter(), slot_state=SlotStates.IS_FULL)
# async def get_anniversary_year(callback: types.CallbackQuery, callback_data: AnniversaryYearCallback, repo: SQLAlchemyRepo, bot: Bot, state: FSMContext, ):
#     await callback.answer()
#     data = await repo.get_repo(CongratulationRepo).get_congratulation_data(slot_id=callback_data.slot_id)
#     await callback.message.answer_photo(photo=data.img_id, caption=data.caption,
#                                         reply_markup=await update_slot_keyboard(slot_id=callback_data.slot_id, current_slot_state=SlotStates.IS_FULL))
#

@anniversary_router.callback_query(SlotUpdateCallback.filter())
async def edit_anniversary_img(callback: types.CallbackQuery, callback_data: AnniversaryYearCallback, repo: SQLAlchemyRepo, bot: Bot, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text=f"Отправьте картинку, в описание вставьте текст поздравления")
    await state.set_state(GetCongratulateData.image)
    await state.update_data(current_slot=callback_data.slot_id)


@anniversary_router.message(ContentTypesFilter(content_types=[ContentType.PHOTO]), state=GetCongratulateData.image)
async def get_congratulate_text(message: types.Message, repo: SQLAlchemyRepo, state: FSMContext):
    data = await state.get_data()
    await repo.get_repo(CongratulationRepo).add_congratulation_data(slot_id=data.get("current_slot"),
                                                                    img_id=message.photo[-1].file_id,
                                                                    caption=message.caption)






