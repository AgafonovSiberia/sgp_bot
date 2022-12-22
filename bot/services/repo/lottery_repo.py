from bot.services.repo.base.repository import BaseSQLAlchemyRepo
from bot.db.models import LotteryList
from sqlalchemy import select, update, func
from bot.models.states import ExpansionModules


class LotteryRepo(BaseSQLAlchemyRepo):
    async def add_module_settings(self, user_id: int, code: int):
        await self._session.merge(LotteryList(user_id=user_id, code=code))
        await self._session.commit()

    async def check_user_in_lottery(self, user_id: int):
        check = bool(await self._session.get(LotteryList, user_id))
        return check

    async def update_ticket_file_id(self, user_id: int, file_id: str):
        await self._session.execute(update(LotteryList).
                                    where(LotteryList.user_id==user_id).
                                    values(ticket_file_id=file_id))
        await self._session.commit()




