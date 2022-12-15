from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.methods import ApproveChatJoinRequest, DeclineChatJoinRequest, RevokeChatInviteLink
from aiogram.dispatcher.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.dispatcher.filters import LEFT, MEMBER
from aiogram.methods import UnbanChatMember

from bot.config_reader import config

from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.filters.channel.link_creator import LinkCreatorFilter

from bot.utils.validators import validator_join_request
from bot.services.methods import request_methods
from bot.services.methods import join_methods
from bot.google_sheets_api import gsheets_api
from bot.utils import notify_admins
from bot import templates
from aiogram import loggers

join_router = Router()
join_router.chat_join_request.bind_filter(LinkCreatorFilter)
join_router.chat_member.bind_filter(LinkCreatorFilter)


@join_router.chat_join_request(link_creator="bot")
async def join_request(update: types.ChatJoinRequest, repo: SQLAlchemyRepo, bot: Bot):
    """
    Заявка на вступление через ссылку-приглашение от бота.
    Проверяем есть ли такой invite_link в заявках(в DB), если есть - добавляем
    ** по умолчанию valid.is_valid всегда True, но можно дописать в validator кастомные параметры
    (TTL заявки, проверку её повторного использование и др.)
    """
    valid = await validator_join_request(from_user_id=update.from_user.id, link=update.invite_link, repo=repo)
    if valid.is_valid:
        return await ApproveChatJoinRequest(chat_id=update.chat.id, user_id=update.from_user.id)

    await DeclineChatJoinRequest(chat_id=update.chat.id, user_id=update.from_user.id)
    await bot.send_message(chat_id=update.from_user.id,
                           text=await bot.templates.text.exceptions_text.not_join_request(valid.error_text))


@join_router.chat_join_request(link_creator="not_bot")
async def join_request(update: types.ChatJoinRequest, repo: SQLAlchemyRepo, bot: Bot):
    """Заявка на вступление через ссылку-приглашение, созданную одним из администраторов"""
    await DeclineChatJoinRequest(chat_id=update.chat.id, user_id=update.from_user.id)
    await bot.send_message(chat_id=update.from_user.id,
                           text=await templates.channel.join_texts.admin_not_approve_join())
    loggers.event.info(
        f"Custom log - module:{__name__} - Заявка на вступление от {update.new_chat_member.user.username} отклонена, так как "
        f"была использована ссылка, созданная одним из администраторов")



@join_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=LEFT >> MEMBER),
                         link_creator="bot")
async def join_invite_from_bot(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    """ Пользователь пришёл по ссылке-приглашению, выданному ботом после регистрации """

    member_pydantic = await join_methods.add_member(update=update, repo=repo)
    await gsheets_api.update_sheets(member_pydantic=member_pydantic)

    await request_methods.delete_request(repo=repo, user_id=update.new_chat_member.user.id)

    await RevokeChatInviteLink(chat_id=config.channel_id, invite_link=update.invite_link.invite_link)
    await notify_admins.send_notify_update(member=member_pydantic, bot=bot, type_update="joined_from_bot")

    loggers.event.info(
        f"Custom log - module:{__name__} - {update.new_chat_member.user.username} - добавлен в канал по ссылке-приглашению,"
        f"выданному ботом после регистрации")

@join_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=LEFT >> MEMBER),
                         link_creator="not_bot")
async def join_invite_from_admin(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo, bot: Bot):
    loggers.event.info(
        f"Custom log - module:{__name__} - {update.new_chat_member.user.username} - пришёл по ссылке от админа")

    await UnbanChatMember(chat_id=update.chat.id, user_id=update.old_chat_member.user.id)

    loggers.event.info(
            f"Custom log - module:{__name__} - {update.new_chat_member.user.username} - был кикнут ботом. В канале включён запрет на добавление в "
            f"обход регистрации через бота")




