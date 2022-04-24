from bot.models.member import MemberPydantic
from bot.services.repo.member_repo import MemberRepo


async def get_notify_text(member: MemberPydantic, type_update: str, ) -> str:
    match type_update:
        case "joined_from_bot":
            text = "\U0001F514 Через бота в канал присоединился новый пользователь\n\n"

        case "joined_from_admin":
            text = "\U0001F514 Через админскую ссылку-приглашение в канал присоединился новый пользователь\n\n"

        case "joined_not_link_user":
            text = "\U0001F514 В канал самовольно присоединился новый пользователь\n\n" \
                   "<i>Возможно, это вызвано багами Telegram. Проверьте пользователя и при необходимости - удалите</i>"

        case "joined_not_link_admin":
            text = "\U0001F514 Администратор добавил в канал нового пользователя\n\n"

        case "to_admin":
            text = "\U0001F4CCВ канале назначен новый администратор\n\n"

        case "member_left_himself":
            text = "\U00002757 Канал самовольно покинул пользователь\n\n<i>В любое время он может снова " \
                   "присоединиться в канал через бота или по прямой ссылке-приглашению</i>\n\n "

        case "kicked_bot":
            text = "\U00002757 Бот исключил из канала пользователя, нарушившего правила регистрации в канале.\n\n" \
                   "<i>В любое время он может снова присоединиться в канал через бота или по прямой " \
                   "ссылке-приглашению</i>\n\n "

        case "banned":
            text = "\U0000274C В канале был заблокирован пользователь\n\n<i>Он больше не сможет войти в канал " \
                   "пока не будет разблокирован администратором</i>\n\n"

        case "unbanned":
            text = "\U00002757 В канале был разблокирован пользователь\n\n<i>Теперь он может снова присоединиться в канал " \
                   "через бота или по ссылке-приглашению от администратора</i>\n\n"

    text = text + f"" \
                  f"\U0001F464 <b>USER:</b>\n" \
                  f"<b>id: </b> {member.user.user_id}\n" \
                  f"<b>Name: </b>{member.user.user_name}\n" \
                  f"<b>Nickname: </b>{member.user.user_nickname}\n" \
                  f"<b>ФИ: </b>{member.user_passport.real_name}\n" \
                  f"<b>Должность: </b>{member.user_passport.position}\n\n" \
                  f"\U0001F478 <b> FROM USER:</b>\n" \
                  f"<b>id: </b>{member.from_user.user_id}\n" \
                  f"<b>Name: </b>{member.from_user.user_name}\n" \
                  f"<b>Nickname: </b>{member.from_user.user_nickname}\n\n" \
                  f"<b>\U000023F1 DATE:</b>\n" \
                  f"{str(member.update_date)}"

    return text
