from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.dispatcher.filters import LEFT, MEMBER, KICKED
from aiogram.methods import BanChatMember

from bot.services.repo.base import SQLAlchemyRepo
from bot.services.methods import update_methods

from bot.filters.user_status import MemberIsOldFilter
from bot.services.workers.tasks import update_member_sheet, send_notify_for_admins


update_router = Router()
update_router.chat_member.bind_filter(MemberIsOldFilter)


@update_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER >> KICKED), member_is_old=True)
async def member_to_kicked_old(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """
    Пользователь заблокирован в канале одним из администраторов/ботом.
    Пользователь не может вернуться в канал, пока не будет разблокирован.
    """
    member_pydantic = await update_methods.update_member(update=update, repo=repo)
    update_member_sheet.delay(member_pydantic=member_pydantic)
    send_notify_for_admins.delay(member=member_pydantic, type_update="banned")


@update_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED >> LEFT), member_is_old=True)
async def kicked_to_left_old(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """
    Пользователь разблокирован в канале одним из администраторов/ботом.
    В любой момент пользователь может вернуться в канал, пройдя регистрацию в боте.
    """
    member_pydantic = await update_methods.update_member(update=update, repo=repo)
    update_member_sheet.delay(member_pydantic=member_pydantic)
    send_notify_for_admins.delay(member=member_pydantic, type_update="unbanned")



@update_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=LEFT >> KICKED), member_is_old=True)
async def kicked_to_left_old(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """
    Администратор заблокировал пользователя, который ранее самовольно покинул канал.
    Обрабатываем блокировку пользователя - вносим данные в БД и таблицу
    """



@update_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER >> LEFT), member_is_old=True)
async def member_to_kicked_old(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """
    Пользователь самовольно покинул канал. Бот блокирует пользователя.
    Пользователь сможет вернуться в канал только обратившись к администратору.
    """
    member_pydantic = await update_methods.update_member(update=update, repo=repo)
    update_member_sheet.delay(member_pydantic=member_pydantic)
    send_notify_for_admins.delay(member=member_pydantic, type_update="left_himself")
    await BanChatMember(chat_id=update.chat.id, user_id=update.old_chat_member.user.id)


@update_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER >> KICKED), member_is_old=False)
async def member_to_kicked_new(update: types.ChatMemberUpdated, bot: Bot):
    """ Бот блокирует пользователя, так как был добавлен в канал одним из администраторов в обход регистрации,
    либо вошёл в канал по основной ссылке-приглашению """
    pass


@update_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED >> LEFT), member_is_old=False)
async def kicked_to_left_new(update: types.ChatMemberUpdated, bot: Bot):
    """Бот разблокирует пользователя, пришедшего в обход регистрации.
    Это даёт возможность пользователю пройти регистрацию нормально"""
    pass



