from bot.service.repo import RequestRepo

from typing import Union, List

from aiogram import types, Bot, loggers
from aiogram.dispatcher.filters import BaseFilter
from aiogram.exceptions import TelegramForbiddenError
from aiogram.methods.get_chat_member import GetChatMember

from bot.database.models import ChannelMember
from bot.service.repo.base import SQLAlchemyRepo
from bot.service.repo import MemberRepo

from bot.config_reader import config

class UserStatusFilter(BaseFilter):
    """User_status in channel (member, left, kicked, administrator"""
    user_status: List[str]
    async def __call__(self, update: Union[types.Message, types.CallbackQuery]) -> bool:
        member = await GetChatMember(chat_id=config.channel_id, user_id=update.from_user.id)
        return member.status in self.user_status

class UserIsUnknownFilter(BaseFilter):
    """Пользователь пришёл в канал через бота или ещё до того, как бота подключили?"""
    user_is_known: bool
    async def __call__(self, message: types.Message, bot: Bot, repo: SQLAlchemyRepo) -> bool:
        bot_data = await bot.get_me()
        member: ChannelMember = await repo.get_repo(MemberRepo).get_member(message.from_user.id)
        check = member.from_user_id == bot_data.id if member else False
        return check == self.user_is_known

class MemberIsOldFilter(BaseFilter):
    member_is_old: bool
    async def __call__(self, update: types.ChatMemberUpdated, repo: SQLAlchemyRepo) -> bool:
        check_member = await repo.get_repo(MemberRepo).check_member(user_id=update.new_chat_member.user.id)
        return check_member == self.member_is_old

class BotStatusFilter(BaseFilter):
    bot_is_admin: bool

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        bot = await bot.get_me()
        status = False
        try:
            member = await GetChatMember(chat_id=config.channel_id, user_id=bot.id)
            status = True if member.status == "administrator" else False
        except TelegramForbiddenError:
            loggers.event.info("Bot is not a member of the methods chat")
        return status == self.bot_is_admin

class LinkCreatorFilter(BaseFilter):
    link_creator: str

    async def __call__(self, update: types.ChatMemberUpdated) -> bool:

        creator_status = "not_bot"
        if update.invite_link:
            creator_status = "bot" if update.invite_link.creator.is_bot else "not_bot"
        return creator_status == self.link_creator


class RequestIsFoundFilter(BaseFilter):
    request_is_found: bool

    async def __call__(self, message: types.Message, repo: SQLAlchemyRepo) -> bool:
        check_request = await repo.get_repo(RequestRepo).check_request(message.chat.id)
        return check_request == self.request_is_found
