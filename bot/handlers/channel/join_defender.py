from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.dispatcher.filters import LEFT, MEMBER, KICKED
from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.filters.channel.member_is_old import MemberIsOld
from aiogram import loggers
from bot.utils import notify_admins
from bot import channel_config
defender_router = Router()
defender_router.chat_member.bind_filter(MemberIsOld)

"""
member_is_old = False - пользователь не был подписан на канал, он попытался войти и был сразу же удалён ботом

Последовательно применяется 2 метода:
- BanChatMember
- UnbanChatMember
Благодаря этому пользователь удаляется из канала с правом вернуться + status=left
**Если использовать просто UnbanChatMember, то статус пользователя будет kicked
"""


@defender_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER >> KICKED), member_is_old=False)
async def member_to_kicked_new(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """ Пользователь пытался подписаться на канал и был сразу же удалён ботом"""
    pass


@defender_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED >> LEFT), member_is_old=False)
async def kicked_to_left_new(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """ Пользователь пытался подписаться на канал и был сразу же удалён ботом
    Причины:
    - включен запрет на прямое приглашение администратором
    - включен запрет на подписку по ссылкам-приглашениям от администраторов (не от бота)

    Тут возможна обработка какой-то специфической логики, например логгирование всех пользователей
    пытавшихся подписать в канал, уведомление администраторов канала и др.
    """
    loggers.event.info(
        f"Custom log - module:{__name__} - Бот отклонил подписку пользователя {update.new_chat_member.user.id}")
