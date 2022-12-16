from aiogram import types, Bot
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.router import Router
from aiogram.methods.get_chat import GetChat
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters.content_types import ContentTypesFilter

from bot.filters.private.user_status import StatusUserFilter
from bot.filters.private.bot_status import BotStatusFilter
from bot.filters.private.request_found import RequestIsFoundFilter

from bot.keyboards.registration_key import generate_phone_key

from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.templates.text import registration_text
from bot.models.states import LeftUserRegistration
from bot.utils.validators import validator_name_user, validator_position_user, validator_contact_user
from bot.services.methods import request_methods
from bot.config_reader import config
from bot.templates import stickers

registration_private_router = Router()
registration_private_router.message.bind_filter(BotStatusFilter)
registration_private_router.message.bind_filter(StatusUserFilter)
registration_private_router.message.bind_filter(RequestIsFoundFilter)

"""
filters:
"bot_added" - добавлен ли бот в канал в качестве админа
"status_user" - статус пользователя (left - вне канала, member - в канале, banned - забанен, kicked - был удалён)
"request_is_found" - регистрация уже была пройдена ранее - invite_link выдана
"""

@registration_private_router.message(commands="start", bot_added=True, status_user=["left"], request_is_found=False)
async def get_new_request(message: types.Message, state: FSMContext):
    await state.clear()
    chat = await GetChat(chat_id=config.channel_id)
    await message.answer_sticker(sticker=stickers.START_STICKER)
    await message.answer(await registration_text.start_message(message.from_user.username, chat.title))
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(LeftUserRegistration.name_user)


@registration_private_router.message(state=LeftUserRegistration.name_user)
async def get_name_user(message: types.Message, state: FSMContext):
    valid = await validator_name_user(message.text)
    if not valid.is_valid:
        await message.answer_sticker(sticker=stickers.NOT_VALID)
        await message.answer(await registration_text.not_valid(valid.error_text))
        return

    await message.answer_sticker(sticker=stickers.GET_POSITION)
    await message.answer(await registration_text.get_position(message.text))
    await state.update_data(user_name=message.text)
    await state.set_state(LeftUserRegistration.position_user)




@registration_private_router.message(state=LeftUserRegistration.position_user)
async def get_position_user(message: types.Message, state: FSMContext):
    valid = await validator_position_user(message.text)
    if not valid.is_valid:
        await message.answer_sticker(sticker=stickers.NOT_VALID)
        await message.answer(await registration_text.not_valid(valid.error_text))
        return

    await message.answer_sticker(sticker=stickers.GET_CONTACT)
    await message.answer(text=registration_text.GET_PHONE_NUMBER, reply_markup=await generate_phone_key())
    await state.update_data(user_position=message.text)
    await state.set_state(LeftUserRegistration.phone_number)


@registration_private_router.message(ContentTypesFilter(content_types=["contact"]), state=LeftUserRegistration.phone_number)
async def get_number_user(contact: types.Contact, state: FSMContext, bot: Bot, repo: SQLAlchemyRepo):
    valid = await validator_contact_user(contact.contact.user_id, contact.chat.id)
    if not valid.is_valid:
        await contact.answer_sticker(sticker=stickers.NOT_VALID)
        await contact.answer(await registration_text.not_valid(valid.error_text))
        return

    await state.update_data(user_phone_number=contact.contact.phone_number)
    await contact.answer_sticker(sticker=stickers.FINALLY_REGISTRATION)
    await contact.answer(registration_text.FINISH_REGISTRATION, reply_markup=ReplyKeyboardRemove)
    link = await request_methods.save_request(bot=bot, state=state, repo=repo)
    await request_methods.send_invite_link(bot=bot, chat_id=contact.chat.id, invite_link=link.invite_link)
    await state.clear()





