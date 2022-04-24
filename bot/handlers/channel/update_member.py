from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.dispatcher.filters import LEFT, MEMBER, KICKED
from bot import channel_config
from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.services.methods import update_methods

from bot.filters.channel.member_is_old import MemberIsOld

from bot.utils import notify_admins

from bot.google_sheets_api import gsheets_api

update_router = Router()
update_router.chat_member.bind_filter(MemberIsOld)

"""
member_is_old = True - пользователь ранее был подписан на канал, удаление происходит по инициативе админа

join_defender.py
c фильтром member_is_old = False - пользователь не был подписан на канал, он попытался войти и был сразу же удалён ботом
Последовательно применяется 2 метода:
- BanChatMember
- UnbanChatMember
Благодаря этому пользователь удаляется из канала с правом вернуться + status=left
**Если использовать просто UnbanChatMember, то статус пользователя будет kicked

"""


@update_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER >> KICKED), member_is_old=True)
async def member_to_kicked_old(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """
    User забанен в канале одним из администраторов.
    User не может вернуться в канал пока не будет предварительно разбранен.
    """
    member_pydantic = await update_methods.update_member(update=update, repo=repo)
    await gsheets_api.update_sheets(member_pydantic=member_pydantic)
    await notify_admins.send_notify(member=member_pydantic, bot=bot, type_update="banned")


@update_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED >> LEFT), member_is_old=True)
async def kicked_to_left_old(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """
    User разбанен в канале.
    В любой момент пользователь может вернуться в канал через бота или ссылке-приглашению от администратора (если разрешено)
    """
    member_pydantic = await update_methods.update_member(update=update, repo=repo)
    await gsheets_api.update_sheets(member_pydantic=member_pydantic)
    await notify_admins.send_notify(member=member_pydantic, bot=bot, type_update="unbanned")



@update_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER >> LEFT), member_is_old=True)
async def member_to_kicked_old(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """
    User добровольно покинул канал
    В любой момент пользователь может вернуться в канал через бота или ссылке-приглашению от администратора (если разрешено)
    """
    member_pydantic = await update_methods.update_member(update=update, repo=repo)
    await gsheets_api.update_sheets(member_pydantic=member_pydantic)
    await notify_admins.send_notify(member=member_pydantic, bot=bot, type_update="member_left_himself")



