from bot.misc.pydantic_models import MemberPydantic
from bot.misc.states import ValidInputError

BOT_IS_NOT_ADMIN = "\U0001F6AB Бот не является администратором вашего канала.\n\n" \
                    "<i>Возможно, бот не был добавлен в канал, либо заблокирован владельцем канала. " \
                    "Обратитесь к создателю канала.</i>"

BANNED_USER = f"<b>ВНИМАНИЕ!</b>\nДанный метод заблокирует пользователя в канале, даже если на данный момент " \
           f"пользователь уже не является подписчиком.\n\n\"" \
           f"Введите <b>USER_ID</b> пользователя, которого необходимо заблокировать:"


async def start_message(username: str = "dear friend", chat_title: str = ""):
    return f"Привет, {username}.\n\nЯ бот-администратор канала <b>{chat_title}</b>"


async def banned_user():
    return f"<b>ВНИМАНИЕ!</b>\nДанный метод заблокирует пользователя в канале, даже если на данный момент " \
           f"пользователь уже не является подписчиком.\n\n\"" \
           f"Введите <b>USER_ID</b> пользователя, которого необходимо заблокировать:"


async def profile_text(member: MemberPydantic):
    return f"\U0001F464 <b>USER:</b>\n" \
           f"<b>id: </b> {member.user.user_id}\n" \
           f"<b>Name: </b>{member.user.user_name}\n" \
           f"<b>Nickname: </b>{member.user.user_nickname}\n" \
           f"<b>ФИ: </b>{member.user_passport.real_name}\n" \
           f"<b>Должность: </b>{member.user_passport.position}\n"


async def not_is_id(valid: ValidInputError):
    return f"Неправильный формат <b>USER_ID</b>\n\n" \
           f"<i>{valid.error_text}</i>\n\n" \
           f"Убедитесь в правильности ID и попробуйте ещё раз"
