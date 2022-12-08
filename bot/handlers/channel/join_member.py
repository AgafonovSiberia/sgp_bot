from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.methods import ApproveChatJoinRequest, DeclineChatJoinRequest, RevokeChatInviteLink
import asyncio
from aiogram.dispatcher.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.methods import UnbanChatMember, BanChatMember
from aiogram.dispatcher.filters import LEFT, MEMBER

from bot import channel_config
from bot.texts.private import exceptions_text
from bot.texts.channel import join_texts

from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.filters.channel.link_creator import LinkCreatorFilter

from bot.utils.validators import validator_join_request
from bot.services.methods import request_methods
from bot.services.methods import join_methods
from bot.google_sheets_api import gsheets_api
from bot.utils import notify_admins
from bot import texts
from aiogram import loggers

join_router = Router()
join_router.chat_join_request.bind_filter(LinkCreatorFilter)
join_router.chat_member.bind_filter(LinkCreatorFilter)


@join_router.chat_join_request(link_creator="bot")
async def join_request(update: types.ChatJoinRequest, repo: SQLAlchemyRepo, bot: Bot):
    """
    Заявка на вступление через ссылку-приглашение от бота (если channel_config.channel_join_request == True)
    Проверяем есть ли такой invite_link в заявках(в DB), если есть - добавляем
    ** в базовой конфигурации valid.is_valid всегда True, но есть возможность дописать в validator кастомные параметры
    (TTL заявки, check её повторного использование и др.)
    """
    valid = await validator_join_request(from_user_id=update.from_user.id, link=update.invite_link, repo=repo)
    if valid.is_valid:
        await ApproveChatJoinRequest(chat_id=update.chat.id, user_id=update.from_user.id)
    else:
        await DeclineChatJoinRequest(chat_id=update.chat.id, user_id=update.from_user.id)
        await bot.send_message(chat_id=update.from_user.id,
                               text=await texts.private.exceptions_text.not_join_request(valid.error_text))


@join_router.chat_join_request(link_creator="administrator")
async def join_request(update: types.ChatJoinRequest, repo: SQLAlchemyRepo, bot: Bot):
    """
    Заявка на вступление через ссылку-приглашение, созданную одним из администраторов
    -> Если в конфиге боту разрешено подтверждать запросы пользователей, пришедших через админскую ссылку-приглашение - добавляем,
    если нет - игнорируем запрос (один из администраторов должен подтвердить / отклонить такой запрос собственноручно)
    """
    if channel_config.bot_approve_join_request:
        await ApproveChatJoinRequest(chat_id=update.chat.id, user_id=update.from_user.id)
    else:
        await DeclineChatJoinRequest(chat_id=update.chat.id, user_id=update.from_user.id)
        await bot.send_message(chat_id=update.from_user.id,
                               text=await texts.channel.join_texts.admin_not_approve_join())


@join_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=LEFT >> MEMBER),
                         link_creator=["bot"])
async def join_invite_from_bot(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """
    User пришёл по ссылке от бота
    -> Если в конфиге включено удаление заявки после join'а, то удаляем заявку из DB
    ** если удаляем, то при возвращении в канал после "Покинуть канал" или UnbanChatMember - User снова проходит регистрацию в боте
    ** если не удаляем, то при возвращении пользователь получает свою старую ссылку и входит в канал со старыми данными регистрации
    """
    loggers.event.info(
        f"Custom log - module:{__name__} - {update.new_chat_member.user.username} - пришёл по ссылке от бота")

    member_pydantic = await join_methods.add_member(update=update, repo=repo)
    await gsheets_api.update_sheets(member_pydantic=member_pydantic)
    if channel_config.delete_request_after_join:
        await request_methods.delete_request(repo=repo, user_id=update.new_chat_member.user.id)

        loggers.event.info(
            f"Custom log - module:{__name__} - Заявка на вступление от {update.new_chat_member.user.username} удалена. После выхода или UnbanChatMember "
            f"пользователь должен будет снова пройти регистрацию через бота")

    await RevokeChatInviteLink(chat_id=channel_config.channel_id, invite_link=update.invite_link.invite_link)
    await notify_admins.send_notify(member=member_pydantic, bot=bot, type_update="joined_from_bot")


@join_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=LEFT >> MEMBER),
                         link_creator=["administrator"])
async def join_invite_from_admin(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """
    User пришёл по основной ссылке-приглашению или ссылке созданной одним из администраторов
    -> Если в конфиге разрешено - оставляем, если нет - удаляем с правом вернуться (method UnbanChatMember)
    """

    loggers.event.info(
        f"Custom log - module:{__name__} - {update.new_chat_member.user.username} - пришёл по ссылке от админа")

    if not channel_config.channel_join_invite_from_admin:
        await BanChatMember(chat_id=update.chat.id, user_id=update.old_chat_member.user.id)
        await asyncio.sleep(0.5)
        await UnbanChatMember(chat_id=update.chat.id, user_id=update.old_chat_member.user.id)

        loggers.event.info(
            f"Custom log - module:{__name__} - {update.new_chat_member.user.username} - был кикнут ботом. В канале включён запрет на добавление в "
            f"обход регистрации через бота")

    else:
        member_pydantic = await join_methods.add_member(update=update, repo=repo)
        await gsheets_api.update_sheets(member_pydantic=member_pydantic)
        await notify_admins.send_notify(member=member_pydantic, bot=bot, type_update="joined_from_admin")


@join_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=LEFT >> MEMBER),
                         link_creator=["not_link_user"])
async def join_not_invite(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """
    User вошёл сам. По-хорошему, в закрытый канал - это невозможно, однако наблюдался баг телеги, 
    когда пользователь присоединялся в закрытый канал через пересланное сообщение из чата обсуждения, закреплённого 
    за каналом.
    -> Если в конфиге разрешено подписывать без ссылки-приглашения, то оставляем, если нет - удаляем с 
    правом вернуться (UnbanChatMember) """

    loggers.event.info(
        f"Custom log - module:{__name__} - {update.new_chat_member.user.username} - пользователь подписался самостоятельно")

    if not channel_config.channel_join_not_link:
        await BanChatMember(chat_id=update.chat.id, user_id=update.old_chat_member.user.id)
        await asyncio.sleep(0.5)
        await UnbanChatMember(chat_id=update.chat.id, user_id=update.old_chat_member.user.id)
    else:
        member_pydantic = await join_methods.add_member(update=update, repo=repo)
        await gsheets_api.update_sheets(member_pydantic=member_pydantic)
        await notify_admins.send_notify(member=member_pydantic, bot=bot, type_update="joined_not_link_user")


@join_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=LEFT >> MEMBER),
                         link_creator=["not_link_administrator"])
async def join_not_invite(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """User был напрямую приглашён одним из администраторов
    -> Если в конфиге разрешено приглашать напрямую то оставляем,
     если нет - удаляем с правом вернуться (UnbanChatMember) """

    loggers.event.info(
        f"Custom log - module:{__name__} - {update.new_chat_member.user.username} - был добавлен админом")

    if not channel_config.channel_join_not_link:
        await BanChatMember(chat_id=update.chat.id, user_id=update.old_chat_member.user.id)
        await asyncio.sleep(0.5)
        await UnbanChatMember(chat_id=update.chat.id, user_id=update.old_chat_member.user.id)
    else:
        member_pydantic = await join_methods.add_member(update=update, repo=repo)
        await gsheets_api.update_sheets(member_pydantic=member_pydantic)
        await notify_admins.send_notify(member=member_pydantic, bot=bot, type_update="joined_not_link_admin")



