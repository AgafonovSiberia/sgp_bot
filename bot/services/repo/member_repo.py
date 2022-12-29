from .base.base_repository import BaseSQLAlchemyRepo
from bot.db.models import ChannelMember
from bot.models.member import MemberPydantic


class MemberRepo(BaseSQLAlchemyRepo):
    async def add_member(self, data: MemberPydantic) -> ChannelMember:
        await self._session.merge(ChannelMember(data=data))
        await self._session.commit()

    async def update_member(self, data: MemberPydantic) -> ChannelMember:
        member = await self._session.get(ChannelMember, data.user.user_id)
        member.user_tg_name = data.user.user_name
        member.user_tg_nickname = data.user.user_nickname
        member.user_status = data.user_status
        member.from_user_id = data.from_user.user_id
        member.from_user_name = data.from_user.user_name
        member.from_user_nickname = data.from_user.user_nickname
        member.update_date = data.update_date
        await self._session.commit()
        return member

    async def check_member(self, user_id: int) -> bool:
        check = bool(await self._session.get(ChannelMember, user_id))
        return check

    async def get_member(self, user_id: int) -> ChannelMember:
        member = await self._session.get(ChannelMember, user_id)
        return member

