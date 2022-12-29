
from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.methods import UnbanChatMember

from bot.models.states import LeftUserRegistration
from bot.services.methods.request_methods import send_invite_link
from aiogram.dispatcher.filters.content_types import ContentTypesFilter

from bot.filters import StatusUserFilter, BotStatusFilter, RequestIsFoundFilter, UserIsUnknownFilter


from bot.services.repo.base import SQLAlchemyRepo
from bot.services.repo import RequestRepo

from bot.templates import stickers
from bot.handlers.registration.registration import get_new_request
from bot.config_reader import config

from bot.templates.text.to_exception import member_is_unknown

exceptions_private_router = Router()
exceptions_private_router.message.bind_filter(BotStatusFilter)
exceptions_private_router.message.bind_filter(UserIsUnknownFilter)
exceptions_private_router.message.bind_filter(StatusUserFilter)
exceptions_private_router.message.bind_filter(RequestIsFoundFilter)


@exceptions_private_router.message(commands="start", bot_added=True,
                                   status_user="member",user_is_known=False)
async def user_status_is_member(message: types.Message, state: FSMContext, bot: Bot):
    """Пользователь уже подписан на канал, но, возможно, подписался раньше, чем запустили бота"""

    await message.answer_sticker(sticker=stickers.USER_IS_JOINED)
    await message.answer(text=await member_is_unknown(username=message.from_user.username))
    await UnbanChatMember(chat_id=config.channel_id, user_id=message.from_user.id)
    await get_new_request(message=message, state=state)



@exceptions_private_router.message(commands="start", bot_added=False)
async def bot_is_blocked(message: types.Message):
    """Бот не является администратором канала или не добавлен в канал"""
    await message.answer(await exception.BOT_NOT_ADDED)


@exceptions_private_router.message(commands="start", bot_added=True, status_user="left", request_is_found=True)
async def request_is_found(message: types.Message, repo: SQLAlchemyRepo, bot: Bot):
    """Заявка уже была подана ранее, ссылка-приглашение выдана и не активирована"""
    user = await repo.get_repo(RequestRepo).get_request(message.chat.id)
    await message.answer(text=await exception.request_is_fount(message.chat.username))
    await send_invite_link(bot=bot, chat_id=message.chat.id, invite_link=user.invite_link)





@exceptions_private_router.message(commands="start", bot_added=True, status_user=["kicked", "banned"])
async def user_status_is_member(message: types.Message):
    """Пользователь заблокирован в канале"""
    await message.answer(text=await exception.member_is_kicked(message.chat.username))


@exceptions_private_router.message(ContentTypesFilter(content_types=types.ContentType.ANY),
                                   state=LeftUserRegistration.phone_number)
async def message_is_not_contact(contact: types.Contact):
    """Сообщение не содержит контакт"""
    await contact.answer(exception.MESSAGE_IS_NOT_CONTACT)
