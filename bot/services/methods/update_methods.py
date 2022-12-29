from aiogram import types

from bot.services.repo.base import SQLAlchemyRepo
from bot.services.repo import MemberRepo

from bot.utils import to_pydantic


async def update_member(update: types.ChatMemberUpdated, repo: SQLAlchemyRepo):
    member_pydantic = await to_pydantic.update_to_member_pydantic(update)
    member_model = await repo.get_repo(MemberRepo).update_member(data=member_pydantic)
    member_pydantic = await to_pydantic.channel_member_model_to_member_pydantic(member_model)
    return member_pydantic
