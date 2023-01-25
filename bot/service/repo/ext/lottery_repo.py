from bot.service.repo.base.repository import BaseSQLAlchemyRepo
from bot.database.models import Lottery
from sqlalchemy import select, update, func


class LotteryRepo(BaseSQLAlchemyRepo):
    async def add_user_ticket(self, user_id: int):
        user = await self._session.merge(Lottery(user_id=user_id))
        await self._session.commit()
        return user

    async def check_user_in_lottery(self, user_id: int):
        user = await self._session.execute(select(Lottery.user_id).where(Lottery.user_id == user_id))
        return bool(user.first())


    async def update_ticket_file_id(self, user_id: int, file_id: str):
        await self._session.execute(update(Lottery).
                                    where(Lottery.user_id==user_id).
                                    values(ticket_file_id=file_id))
        await self._session.commit()

    async def get_ticket_file_id(self, user_id: int):
        ticket_file_id = await self._session.execute(select(Lottery.ticket_file_id).where(Lottery.user_id==user_id))
        return ticket_file_id.scalar()

    async def lottery_list_reset(self):
        await self._session.execute("""TRUNCATE TABLE  lottery_list""")
        await self._session.commit()








