BOT_NOT_ADDED = "Бот был заблокирован создателем и больше не является администратором канала"

MESSAGE_IS_NOT_CONTACT = "Мне нужно, чтобы ты прислал свой контакт нажатием кнопки <b>'Поделиться моим " \
                         "контактом'</b>\n\nДавай попробуем ещё раз\n\U000023EC\U000023EC\U000023EC"



async def request_is_fount(username: str) -> str:
    return f"<b>{username}</b>, ты уже прошёл регистрацию ранее и получил своё приглашение в канал."


async def status_is_member(username: str) -> str:
    return f"<b>{username}</b>, ты уже подписан на канал"


async def member_is_kicked(username: str) -> str:
    return f"<b>{username}</b>, ты заблокирован в канале.\n\n" \
           f"<i>За дополнительной информацией ты можешь обратиться к HR</i>"

