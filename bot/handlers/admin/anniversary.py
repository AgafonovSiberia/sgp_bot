from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.fsm.context import FSMContext
from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.services.repo.congratulation_repo import CongratulationRepo
from bot.db.models import CongratulationData
from magic_filter import F


from bot.keyboards.anniversary_key import anniversary_years_key,anniversary_edit_params_key,\
    AnniversaryYearCallback, AnniversaryEditCallback


anniversary_router = Router()

@anniversary_router.callback_query(F.data == "congratulation")
async def congratulation_params(callback: types.CallbackQuery, state=FSMContext):
    await callback.answer()
    await callback.message.answer(text="Какой год лалал", reply_markup=await anniversary_years_key())



@anniversary_router.callback_query(AnniversaryYearCallback.filter())
async def get_anniversary_year(callback: types.CallbackQuery, callback_data: AnniversaryYearCallback, repo: SQLAlchemyRepo, bot: Bot, state: FSMContext, ):
    await callback.answer()
    print(callback_data.year)
    data: CongratulationData = await repo.get_repo(CongratulationRepo).get_congratulation_data(year=callback_data.year)
    if not data:
        await callback.message.answer(text="Данные отсутствуют в базе данных", reply_markup=await anniversary_edit_params_key(year=callback_data.year))
        return

    await callback.answer(text=data.text)

@anniversary_router.callback_query(AnniversaryEditCallback.filter(F.data_type == "text"))
async def edit_anniversary_text(callback: types.CallbackQuery, callback_data: AnniversaryYearCallback, repo: SQLAlchemyRepo, bot: Bot, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text=f"Отправьте в следующем сообщении текст поздравления {callback_data.year}, {callback_data.data_type}")


@anniversary_router.callback_query(AnniversaryEditCallback.filter(F.data_type == "img"))
async def edit_anniversary_img(callback: types.CallbackQuery, callback_data: AnniversaryYearCallback, repo: SQLAlchemyRepo, bot: Bot, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text=f"Отправьте картинку {callback_data.year}, {callback_data.data_type}")






