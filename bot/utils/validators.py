from bot.models.errors import ValidInputError
from aiogram import types
from bot.services.repo.base import SQLAlchemyRepo
from bot.services.repo import RequestRepo


async def validator_is_id(user_id: str) -> ValidInputError:
    if not user_id.isdigit():
        return ValidInputError(is_valid=False,
                               error_text="user_id может содержать только цифры")
    return ValidInputError(is_valid=True,
                           error_text="")


async def validator_name_user(name) -> ValidInputError:
    """
    :param name: first_name + last_name user
    :return: ValidInputError
    all literals is alpha
    length name >= 4 literals
    """
    name = name.replace(" ", "")
    if not (name.isalpha()):
        return ValidInputError(is_valid=False,
                               error_text="Запрещено использовать любые знаки, кроме букв латиницы/кириллицы")
    elif len(name) < 4:
        return ValidInputError(is_valid=False,
                               error_text="Фамилия и имя не могут быть короче 4 символов")
    return ValidInputError(is_valid=True, error_text=None)


async def validator_position_user(position) -> ValidInputError:
    """
        :param position user
        :return: ValidInputError
        length position >= 4 literals
        """
    position = position.replace(" ", "")
    if len(position) < 4:
        return ValidInputError(is_valid=False,
                               error_text="Название должности не может быть короче 4 символов."
                                          "<i> Ты можешь указать город/подразделение/отдел</i>")
    return ValidInputError(is_valid=True, error_text=None)


async def validator_contact_user(contact_id, user_id) -> ValidInputError:
    if contact_id == user_id:
        return ValidInputError(is_valid=True, error_text=None)
    return ValidInputError(is_valid=False,
                           error_text="ID владельца контакта не совпадает с вашим Telegram-ID. "
                                      "Воспользуйтесь кнопкой <b>'Поделиться моим контактом'</b>"
                                      "\n\U000023EC\U000023EC\U000023EC")


async def validator_join_request(from_user_id: int, link: types.ChatInviteLink,
                                 repo: SQLAlchemyRepo) -> ValidInputError:
    """
    :param from_user_id:
    :param link: types.ChatInviteLink
    :param repo: SQLAlchemuRepo
    :return:
    если пользователь пришёл по ссылке
    если ссылка из апдейта совпадает со ссылкой в заявке
    """
    request = await repo.get_repo(RequestRepo).get_request(from_user_id)
    if link and request and link.invite_link == request.invite_link:
        return ValidInputError(is_valid=True,
                               error_text="")
    else:
        return ValidInputError(is_valid=False,
                               error_text="В канал можно присоединиться только по ссылке-приглашению от "
                                          "бота-администратора")
