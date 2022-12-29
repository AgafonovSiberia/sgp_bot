from aiogram import types, Bot
from aiogram.dispatcher.router import Router
from aiogram.methods import GetChat

from bot.filters.user_status import StatusUserFilter, BotStatusFilter
from bot.filters import LotteryActiveFilter
from bot.templates import stickers
from bot.templates.text import user_text
from bot.services.repo.base.repository import SQLAlchemyRepo

from bot.filters import UserIsUnknownFilter
from bot.keyboards.user_key import user_main_keyboard
from bot.config_reader import config

user_panel_router = Router()
user_panel_router.message.bind_filter(UserIsUnknownFilter)
user_panel_router.message.bind_filter(BotStatusFilter)
user_panel_router.message.bind_filter(StatusUserFilter)
user_panel_router.message.bind_filter(LotteryActiveFilter)



@user_panel_router.message(commands="start", bot_added=True, status_user="member",
                           user_is_known=True)
async def user_main_panel(message: types.Message, repo: SQLAlchemyRepo):
    chat = await GetChat(chat_id=config.channel_id)
    await message.answer_sticker(sticker=stickers.START_STICKER)
    await message.answer(text=await user_text.user_start_message(message.from_user.username, chat.title),
                         reply_markup=await user_main_keyboard(chat_link=chat.invite_link, repo=repo))






