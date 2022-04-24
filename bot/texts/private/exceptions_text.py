
async def bot_not_added() -> str:
    return f"Бот был заблокирован создателем и больше не является администратором канала"


async def request_is_fount(username) -> str:
    return f"<b>{username}</b>, ты уже прошёл регистрацию ранее и получил своё приглашение в канал."


async def status_is_member(username) -> str:
    return f"<b>{username}</b>, ты уже подписан на канал"


async def member_is_kicked(username) -> str:
    return f"<b>{username}</b>, ты заблокирован в канале.\n\n" \
           f"<i>За дополнительной информацией ты можешь обратиться к HR</i>"


async def message_is_not_contact() -> str:
    return f"Мне нужно, чтобы ты прислал свой контакт нажатием кнопки <b>'Поделиться моим " \
           "контактом'</b>\n\nДавай попробуем ещё раз\n\U000023EC\U000023EC\U000023EC"




