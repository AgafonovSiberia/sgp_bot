from typing import Union, List

from aiogram import types, Bot, loggers
from aiogram.dispatcher.filters import BaseFilter
from aiogram.exceptions import TelegramForbiddenError
from bot.db.models import ChannelMember
from aiogram.methods.get_chat_member import GetChatMember


from bot.config_reader import config
from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.services.repo.member_repo import MemberRepo


class StatusUserFilter(BaseFilter):
    """User_status in channel (member, left, kicked, administrator"""
    status_user: Union[str, List[str]]
    async def __call__(self, update: Union[types.Message, types.CallbackQuery]) -> bool:
        member = await GetChatMember(chat_id=config.channel_id, user_id=update.from_user.id)
        return member.status in self.status_user

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
    bot_added: bool

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        bot = await bot.get_me()
        status = False
        try:
            member = await GetChatMember(chat_id=config.channel_id, user_id=bot.id)
            status = True if member.status == "administrator" else False
        except TelegramForbiddenError:
            loggers.event.info(
                f"Custom log - module:{__name__} - Bot is not a member of the methods chat")
        return status == self.bot_added
