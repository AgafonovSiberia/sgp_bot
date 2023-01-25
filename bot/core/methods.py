from aiogram import types, Bot
from aiogram.dispatcher.fsm.context import FSMContext

from bot.misc.pydantic_models import MemberPydantic

from bot.core.keyboards import generate_invite_link_key

from bot.templates.text import to_registration

from bot.service.repo.base import SQLAlchemyRepo
from bot.service.repo import MemberRepo, RequestRepo

from bot.utils import model_converter

from bot.config_reader import config

async def save_request(bot: Bot, state: FSMContext, repo: SQLAlchemyRepo) -> types.ChatInviteLink:
    link = await generate_invite_link(bot=bot)
    data = await state.get_data()
    await repo.get_repo(RequestRepo).add_request(user_id=data.get("user_id"),
                                                 user_name=data.get("user_name"),
                                                 user_position=data.get("user_position"),
                                                 user_phone_number=data.get("user_phone_number"),
                                                 invite_link=link.invite_link)

    return link

async def add_member(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo) -> MemberPydantic:
    request = await repo.get_repo(RequestRepo).get_request(user_id=update.new_chat_member.user.id)
    member = await model_converter.update_to_member_pydantic(update, request)
    await repo.get_repo(MemberRepo).add_member(member)
    return member

async def update_member(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo):
    member_pydantic = await model_converter.update_to_member_pydantic(update)
    member_model = await repo.get_repo(MemberRepo).update_member(data=member_pydantic)
    member_pydantic = await model_converter.channel_member_model_to_member_pydantic(member_model)
    return member_pydantic

async def generate_invite_link(bot: Bot) -> types.ChatInviteLink:
    return await bot.create_chat_invite_link(chat_id=config.channel_id,
                                             creates_join_request=True)

async def send_invite_link(bot: Bot, chat_id: int, invite_link: str):
    await bot.send_message(chat_id=chat_id, text=to_registration.SEND_LINK,
                           reply_markup=await generate_invite_link_key(invite_link))

async def delete_request(user_id: int, repo: SQLAlchemyRepo):
    await repo.get_repo(RequestRepo).delete_request(user_id=user_id)


