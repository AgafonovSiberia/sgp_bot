from aiogram import types

from bot.services.repo.base import SQLAlchemyRepo
from bot.services.repo import MemberRepo, RequestRepo
from bot.models.member import MemberPydantic

from bot.utils import to_pydantic



async def add_member(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo) -> MemberPydantic:
    request = await repo.get_repo(RequestRepo).get_request(user_id=update.new_chat_member.user.id)
    member = await to_pydantic.update_to_member_pydantic(update, request)
    await repo.get_repo(MemberRepo).add_member(member)
    return member

