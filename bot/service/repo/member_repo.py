import datetime
from .base.base_repository import BaseSQLAlchemyRepo
from bot.database.models import ChannelMember
from bot.misc.pydantic_models import MemberPydantic
from sqlalchemy import update, select, extract
from datetime import datetime as dt

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

    async def update_employment_date(self, user_id: int, employment_date: datetime.date):
        await self._session.execute(update(ChannelMember).
                                    where(ChannelMember.user_id == user_id).
                                    values(employment_date=employment_date))
        await self._session.commit()


    async def get_member_is_anniversary(self):
        members = await self._session.execute(
                                        select([ChannelMember.user_id, extract("year", ChannelMember.employment_date)]).
                                        where(extract("day", ChannelMember.employment_date) == dt.now().day).
                                        where(extract("month", ChannelMember.employment_date) == dt.now().month).
                                        where(extract("year", ChannelMember.employment_date) != dt.now().year).
                                        where(ChannelMember.user_status.in_(("member", "owner", "administrator")))
                                         )

        await self._session.commit()
        return members.all()

