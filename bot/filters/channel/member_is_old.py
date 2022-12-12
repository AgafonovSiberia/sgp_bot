from aiogram import types
from aiogram.dispatcher.filters import BaseFilter

from bot.services.repo.base.repository import SQLAlchemyRepo
from bot.services.repo.member_repo import MemberRepo

class MemberIsOld(BaseFilter):
    member_is_old: bool
    async def __call__(self, update: types.ChatMemberUpdated, repo: SQLAlchemyRepo) -> bool:
        check_member = await repo.get_repo(MemberRepo).check_member(user_id=update.new_chat_member.user.id)
        return check_member == self.member_is_old
