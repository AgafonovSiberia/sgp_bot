from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.dispatcher.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.dispatcher.filters import JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram.methods import LeaveChat
from bot import channel_config
from aiogram import loggers

bot_channel_member_router = Router()


@bot_channel_member_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def joined_bot_to_channel(update: types.ChatMemberUpdated):
    """
    Добавление бота в канал
    Если канал не прописан в конфиге - бот выходит из канала
    ** в текущем варианте подразумевается один инстанс бота на один канал
    """
    if channel_config.channel_id != update.chat.id:
        await LeaveChat(chat_id=update.chat.id)
        loggers.event.info(f"Custom log - module:{__name__} - бот был присоединён в чужой канал ({update.chat.title})")
        return

    loggers.event.info(
        f"Custom log - module:{__name__} - бот был присоединён в Ваш канал ({update.chat.title})")


@bot_channel_member_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION))
async def joined_bot_to_channel(update: types.ChatMemberUpdated):
    """
    Выход / удаление бота из канала
    ** Тут реализуем какую-то логику в случае добавления бота в "другой" канал и его последующего выхода

    """
    if update.from_user.id != update.new_chat_member.user.id:
        loggers.event.info(f"Custom log - module:{__name__} - Бот был удалён из канала {update.chat.title}")
        return
    loggers.event.info(f"Custom log - module:{__name__} - Бот покинул чат {update.chat.title} согласно политике безопасности")

