from bot.services.repo.base.repository import BaseSQLAlchemyRepo
from bot.db.models import CongratulationData


class CongratulationRepo(BaseSQLAlchemyRepo):
    async def add_congratulation_data(self, year:int, text: str, picture_id: str) -> CongratulationData:
        await self._session.merge(CongratulationData(year=year, text=text, picture_id=picture_id))
        await self._session.commit()


    async def get_congratulation_data(self, year:int) -> CongratulationData:
        data = await self._session.get(CongratulationData, year)
        return data


