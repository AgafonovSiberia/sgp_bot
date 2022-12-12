from bot.services.methods.request_methods import send_invite_link
from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from bot.models.states import LeftUserRegistration
from bot.services.repo.request_repo import RequestRepo
from aiogram.dispatcher.filters.content_types import ContentTypesFilter
from bot.filters.private.user_status import StatusUserFilter
from bot.filters.private.bot_status import BotStatusFilter
from bot.filters.private.request_found import RequestIsFoundFilter

from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.templates.text import exceptions_text
from bot.templates import stickers

exceptions_private_router = Router()
exceptions_private_router.message.bind_filter(BotStatusFilter)
exceptions_private_router.message.bind_filter(StatusUserFilter)
exceptions_private_router.message.bind_filter(RequestIsFoundFilter)


@exceptions_private_router.message(commands="start", bot_added=False)
async def bot_is_blocked(message: types.Message):
    """Бот не является администратором канала"""
    await message.answer(await exceptions_text.BOT_NOT_ADDED)


@exceptions_private_router.message(commands="start", bot_added=True, status_user="left", request_is_found=True)
async def request_is_found(message: types.Message, repo: SQLAlchemyRepo, bot: Bot):
    """Заявка уже была подана ранее, ссылка-приглашение выдана и не активирована"""
    user = await repo.get_repo(RequestRepo).get_request(message.chat.id)
    await message.answer(text=await exceptions_text.request_is_fount(message.chat.username))
    await send_invite_link(bot=bot, chat_id=message.chat.id, invite_link=user.invite_link)


@exceptions_private_router.message(commands="start", bot_added=True, status_user="member")
async def user_status_is_member(message: types.Message):
    """Пользователь уже подписан на канал"""
    await message.answer_sticker(sticker=stickers.USER_IS_JOINED)
    await message.answer(text=await exceptions_text.status_is_member(message.chat.username))


@exceptions_private_router.message(commands="start", bot_added=True, status_user=["kicked", "banned"])
async def user_status_is_member(message: types.Message):
    """Пользователь заблокирован в канале"""
    await message.answer(text=await exceptions_text.member_is_kicked(message.chat.username))


@exceptions_private_router.message(ContentTypesFilter(content_types=types.ContentType.ANY),
                                   state=LeftUserRegistration.phone_number)
async def message_is_not_contact(contact: types.Contact):
    """Сообщение не содержит контакт"""
    await contact.answer(await exceptions_text.MESSAGE_IS_NOT_CONTACT)
