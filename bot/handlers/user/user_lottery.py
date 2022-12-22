from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.fsm.context import FSMContext
from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.services.repo.settings_repo import SettingsRepo
from bot.services.repo.lottery_repo import LotteryRepo

from bot.db.models import ModuleSettings, LotteryList
from magic_filter import F

from bot.models.states import ExpansionModules
from bot.filters import StatusUserFilter
from bot.services.methods.lottery_methods import generate_ticket

from bot.google_sheets_api.gsheets_api import add_record_from_lottery

user_lottery_router = Router()
user_lottery_router.callback_query.bind_filter(StatusUserFilter)


@user_lottery_router.callback_query(F.data == "start_lottery")
async def lottery_get_ticket(callback: types.CallbackQuery,  repo: SQLAlchemyRepo, bot: Bot, state:FSMContext):
    """Обрабатываем генерацию случайного номера"""
    data: ModuleSettings = await repo.get_repo(SettingsRepo).increment_current_code()
    """Фильтр на то, что ИГРА АКТИВИРОВАНА"""
    """Фильтр на то, что код уже был получен ранее"""


    img = await bot.get_file(data.config.get("template_id"))
    img = await bot.download_file(file_path=img.file_path)
    current_code = data.config.get("current_code")

    await repo.get_repo(LotteryRepo).add_module_settings(user_id=callback.message.from_user.id,
                                                         code=current_code)

    #это по-хорошему в селери
    ticket = await generate_ticket(img=img, code=current_code)

    #это всё точно в селери
    await add_record_from_lottery(user_id=callback.message.from_user.id, username=callback.message.from_user.username,
                                  code=current_code)


    data = await callback.message.answer_photo(photo=types.BufferedInputFile(file=ticket, filename="ticket"), caption=data.config.get("caption"))

    await repo.get_repo(LotteryRepo).update_ticket_file_id(user_id=callback.message.from_user.id,
                                                           file_id=data.photo[-1].file_id)










