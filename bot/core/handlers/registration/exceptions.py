from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.filters.content_types import ContentTypesFilter

from bot.service.repo.base import SQLAlchemyRepo
from bot.service.repo import RequestRepo

from bot.misc.states import LeftUserRegistration

from bot.core.methods import send_invite_link
from bot.core.filters import UserStatusFilter, RequestIsFoundFilter, UserIsUnknownFilter

from bot.templates.text import to_exception

registration_exception_router = Router()
registration_exception_router.message.bind_filter(UserIsUnknownFilter)
registration_exception_router.message.bind_filter(UserStatusFilter)
registration_exception_router.message.bind_filter(RequestIsFoundFilter)




@registration_exception_router.message(commands="start", user_status=["left"], request_is_found=True)
async def request_is_found(message: types.Message, repo: SQLAlchemyRepo, bot: Bot):
    """Заявка уже была подана ранее, ссылка-приглашение выдана и не активирована"""
    user = await repo.get_repo(RequestRepo).get_request(message.chat.id)
    await message.answer(text=await to_exception.request_is_found(message.chat.username))
    await send_invite_link(bot=bot, chat_id=message.chat.id, invite_link=user.invite_link)


@registration_exception_router.message(commands="start", user_status=["kicked", "banned"])
async def user_status_is_member(message: types.Message):
    """Пользователь заблокирован в канале"""
    await message.answer(text=await to_exception.member_is_kicked(message.chat.username))


@registration_exception_router.message(ContentTypesFilter(content_types=types.ContentType.ANY),
                                       state=LeftUserRegistration.phone_number)
async def message_is_not_contact(contact: types.Contact):
    """Сообщение не содержит контакт"""
    await contact.answer(to_exception.MESSAGE_IS_NOT_CONTACT)
