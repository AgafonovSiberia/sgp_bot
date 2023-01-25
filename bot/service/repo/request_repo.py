from bot.database.models import ChannelRequest
from sqlalchemy import select

from .base.base_repository import BaseSQLAlchemyRepo

class RequestRepo(BaseSQLAlchemyRepo):
    # добавить запросы на добавление в канал в бд
    async def add_request(self,
                          user_id: int,
                          user_name: str,
                          user_position: str = "NotPosition",
                          user_phone_number: str = "NotPhone",
                          invite_link: str = "NotInviteLink") -> ChannelRequest:
        await self._session.merge(ChannelRequest(user_id=user_id,
                                                 user_name=user_name,
                                                 user_position=user_position,
                                                 user_phone_number=user_phone_number,
                                                 invite_link=invite_link))
        await self._session.commit()

    # check request from database
    async def check_request(self, user_id: int) -> bool:
        return bool(await self._session.get(ChannelRequest, user_id))

    # get request-obj ChannelRequest
    async def get_request(self, user_id: int) -> ChannelRequest:
        sql = select(ChannelRequest).where(ChannelRequest.user_id == user_id)
        result = await self._session.execute(sql)
        return result.scalar()

    async def delete_request(self, user_id: int) -> bool:
        request = await self._session.get(ChannelRequest, user_id)
        result = await self._session.delete(request)
        await self._session.commit()
        return result
