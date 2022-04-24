from aiogram import types, Bot
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.router import Router
from aiogram.methods.get_chat import GetChat
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters.content_types import ContentTypesFilter

from bot.filters.private.user_status import StatusUserFilter
from bot.filters.private.bot_status import BotStatusFilter
from bot.filters.private.request_found import RequestIsFoundFilter

from bot.keyboards.left_user_key import generate_phone_key

from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.texts.private import left_user_texts
from bot.models.states import LeftUserRegistration
from bot.services.methods import request_methods
from bot.utils.validators import validator_name_user, validator_position_user, validator_contact_user
from bot.services.methods import request_methods
from bot import channel_config
from bot.texts import stickers


left_user_router = Router()
left_user_router.message.bind_filter(BotStatusFilter)
left_user_router.message.bind_filter(StatusUserFilter)
left_user_router.message.bind_filter(RequestIsFoundFilter)

"""
filters handlers:
"bot_added" - добавлен ли бот в канал
"status_user" - статус пользователя (left - вне канала, member - в канале, banned - забанен)
"request_is_found" - регистрация уже была пройдена ранее - invite_link выдана
"""


# Пришёл сырой пользователь
@left_user_router.message(commands="start", bot_added=True, status_user=["left"], request_is_found=False)
async def get_new_request(message: types.Message, state: FSMContext):
    await state.clear()
    chat = await GetChat(chat_id=channel_config.channel_id)
    await message.answer_sticker(sticker=stickers.main)
    await message.answer(await left_user_texts.start_message(message.from_user.username, chat.title))
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(LeftUserRegistration.name_user)


@left_user_router.message(state=LeftUserRegistration.name_user)
async def get_name_user(message: types.Message, state: FSMContext):
    valid = await validator_name_user(message.text)
    if valid.is_valid:
        await message.answer_sticker(sticker=stickers.get_position)
        await message.answer(await left_user_texts.get_position(message.text))
        await state.update_data(user_name=message.text)
        await state.set_state(LeftUserRegistration.position_user)
    else:
        await message.answer_sticker(sticker=stickers.not_valid)
        await message.answer(await left_user_texts.not_valid(valid.error_text))


@left_user_router.message(state=LeftUserRegistration.position_user)
async def get_position_user(message: types.Message, state: FSMContext):
    valid = await validator_position_user(message.text)
    if valid.is_valid:
        await message.answer_sticker(sticker=stickers.get_contact)
        await message.answer(text=await left_user_texts.get_phone(), reply_markup=await generate_phone_key())
        await state.update_data(user_position=message.text)
        await state.set_state(LeftUserRegistration.phone_number)
    else:
        await message.answer_sticker(sticker=stickers.not_valid)
        await message.answer(await left_user_texts.not_valid(valid.error_text))


# message is Contact
@left_user_router.message(ContentTypesFilter(content_types=["contact"]), state=LeftUserRegistration.phone_number)
async def get_number_user(contact: types.Contact, state: FSMContext, bot: Bot, repo: SQLAlchemyRepo):
    valid = await validator_contact_user(contact.contact.user_id, contact.chat.id)
    if valid.is_valid:
        await state.update_data(user_phone_number=contact.contact.phone_number)
        await contact.answer_sticker(sticker=stickers.finally_registration)
        await contact.answer(await left_user_texts.finish_reg(), reply_markup=ReplyKeyboardRemove)
        link = await request_methods.save_request(bot=bot, state=state, repo=repo)
        await request_methods.send_invite_link(bot=bot, chat_id=contact.chat.id, invite_link=link.invite_link)
        await state.clear()
    else:
        await contact.answer_sticker(sticker=stickers.not_valid)
        await contact.answer(await left_user_texts.not_valid(valid.error_text))




