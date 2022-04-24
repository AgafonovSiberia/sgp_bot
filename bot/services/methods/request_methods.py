from aiogram import types, Bot
from aiogram.dispatcher.fsm.context import FSMContext

from bot.keyboards.left_user_key import generate_invite_link_key

from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.services.repo.request_repo import RequestRepo
from bot.texts.private import left_user_texts

from bot import channel_config

# создаём ссылку приглашение
async def generate_invite_link(bot: Bot) -> types.ChatInviteLink:
    link = await bot.create_chat_invite_link(chat_id=channel_config.channel_id,
                                             creates_join_request=True)
    return link


# создаём ссылку, выдаём ссылку, пишем всё в базу данных
async def save_request(bot: Bot, state: FSMContext, repo: SQLAlchemyRepo) -> types.ChatInviteLink:
    link = await generate_invite_link(bot=bot)
    data = await state.get_data()
    await repo.get_repo(RequestRepo).add_request(user_id=data["user_id"],
                                                 user_name=data["user_name"],
                                                 user_position=data["user_position"],
                                                 user_phone_number=data["user_phone_number"],
                                                 invite_link=link.invite_link)

    return link


# sender invite_link url
async def send_invite_link(bot: Bot, chat_id: int, invite_link: str):
    await bot.send_message(chat_id=chat_id, text=await left_user_texts.send_link(),
                           reply_markup=await generate_invite_link_key(invite_link))


async def delete_request(user_id:int, repo: SQLAlchemyRepo):
    await repo.get_repo(RequestRepo).delete_request(user_id=user_id)
