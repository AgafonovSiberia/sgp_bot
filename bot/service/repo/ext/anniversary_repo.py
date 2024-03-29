from bot.service.repo.base.repository import BaseSQLAlchemyRepo
from bot.database.models import CongratulationData


class AnniversaryRepo(BaseSQLAlchemyRepo):
    async def add_congratulation_data(self, slot_id:int, caption: str, img_id: str) -> CongratulationData:
        await self._session.merge(CongratulationData(slot_id=slot_id, caption=caption, img_id=img_id))
        await self._session.commit()

    async def get_congratulation_data(self, slot_id:int) -> CongratulationData:
        data = await self._session.get(CongratulationData, slot_id)
        return data



