from aiogram import Bot, types
from aiogram.methods import GetChat, UnbanChatMember
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.router import Router

from bot.core.handlers.registration.registration import start_registration
from bot.core.filters import UserStatusFilter, UserIsUnknownFilter
from bot.core.keyboards import user_main_keyboard

from bot.templates import stickers
from bot.templates.text import to_user, to_exception
from bot.service.repo.base import SQLAlchemyRepo

from bot.config_reader import config

user_router = Router()
user_router.message.bind_filter(UserIsUnknownFilter)
user_router.message.bind_filter(UserStatusFilter)

user_router.message.filter(user_status=["member"])

@user_router.message(commands="start", user_is_known=True)
async def user_main_panel(message: types.Message, repo: SQLAlchemyRepo):
    chat = await GetChat(chat_id=config.channel_id)
    await message.answer_sticker(sticker=stickers.START_STICKER)
    await message.answer(text=await to_user.user_start_message(message.from_user.username, chat.title),
                         reply_markup=await user_main_keyboard(chat_link=chat.invite_link, repo=repo))


@user_router.message(commands="start", user_is_known=False)
async def user_status_is_member(message: types.Message, state: FSMContext):
    """
    Принудительная регистрация всех пользователей канала
    Пользователь уже подписан на канал, но подписался раньше, чем в канал запустили бота
    Бот удаляет пользователя из канала -> стартует процедуру регистрации
    :param message:
    :param state:
    :return:
    """
    await message.answer_sticker(sticker=stickers.USER_IS_JOINED)
    await message.answer(text=await to_exception.member_is_unknown(username=message.from_user.username))
    await UnbanChatMember(chat_id=config.channel_id, user_id=message.from_user.id)
    await start_registration(message=message, state=state)




