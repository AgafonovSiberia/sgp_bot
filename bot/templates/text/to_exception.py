BOT_NOT_ADDED = "Бот был заблокирован создателем и больше не является администратором канала"

MESSAGE_IS_NOT_CONTACT = "Мне нужно, чтобы ты прислал свой контакт нажатием кнопки <b>'Поделиться моим " \
                         "контактом'</b>\n\nДавай попробуем ещё раз\n\U000023EC\U000023EC\U000023EC"


async def request_is_found(username: str) -> str:
    return f"<b>{username}</b>, ты уже прошёл регистрацию ранее и получил своё приглашение в канал."


async def status_is_member(username: str) -> str:
    return f"<b>{username}</b>, ты уже подписан на канал"


async def member_is_kicked(username: str) -> str:
    return f"<b>{username}</b>, ты заблокирован в канале.\n\n" \
           f"<i>За дополнительной информацией ты можешь обратиться к одному из HR-менеджеров</i>"

async def member_is_unknown(username: str) -> str:
    return f"<b>{username}</b>, ты пришёл в канал до того, как я появился на свет.\U0001F914 \n" \
           f"Кажется, что я ничего о тебе не знаю.\U0001F9D0\n\n" \
           f"Подожди немного, сейчас я подготовлюсь и задам тебе несколько вопросов."


