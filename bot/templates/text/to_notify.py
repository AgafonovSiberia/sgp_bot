from bot.misc.pydantic_models import MemberPydantic

NOTIFY_ADMINS_TEXT_TEMPLATES = {
    "joined_from_bot":"\U0001F514 Через бота в канал присоединился новый пользователь\n\n",

    "to_admin": "\U0001F4CCВ канале назначен новый администратор\n\n",

    "left_himself": "\U00002757 Канал самовольно покинул пользователь\n\n<i>Он будет заблокирован ботом и больше не сможет" \
                   " самостоятельно вернуться в канал.</i>\n\n ",

    "banned": "\U0000274C В канале был заблокирован пользователь\n\n<i>Он больше не сможет войти в канал " \
                   "пока не будет разблокирован администратором</i>\n\n",

    "unbanned": "\U00002757 В канале был разблокирован пользователь\n\n<i>Теперь он может снова присоединиться в канал, " \
                   "пройдя регистрацию через бота</i>\n\n",
    "defender": "Из канала был удалён пользователь, который был добавлен в канал одним из администраторов в обход регистрации"
}


async def get_notify_text(member: MemberPydantic, type_update: str) -> str:
    notify_text = NOTIFY_ADMINS_TEXT_TEMPLATES.get(type_update) + f"" \
                  f"\U0001F464 <b>USER:</b>\n" \
                  f"<b>id: </b> {member.user.user_id}\n" \
                  f"<b>Name: </b>{member.user.user_name}\n" \
                  f"<b>Nickname: </b>{member.user.user_nickname}\n" \
                  f"<b>ФИ: </b>{member.user_passport.real_name}\n" \
                  f"<b>Должность: </b>{member.user_passport.position}\n\n" \
                  f"\U0001F464 <b> FROM USER:</b>\n" \
                  f"<b>id: </b>{member.from_user.user_id}\n" \
                  f"<b>Name: </b>{member.from_user.user_name}\n" \
                  f"<b>Nickname: </b>{member.from_user.user_nickname}\n\n" \
                  f"<b>\U000023F1 DATE:</b>\n" \
                  f"{member.update_date.strftime('%d/%m/%Y, %H:%M:%S')}"

    return notify_text
