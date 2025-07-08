from sqlalchemy.ext.asyncio import AsyncSession
from blog.domain.entities.history import History
from blog.domain.repositories.history_repository import HistoryRepository
from blog.infra.models.history_model import HistoryModel
from sqlalchemy.future import select

class SQLAlchemyHistoryRepository(HistoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_to_history(self, history: History) -> History:
        history_model = HistoryModel.from_entity(history)
        self.session.add(history_model)
        await self.session.commit()
        return history_model.to_entity()

    async def get_user_history(self, user_id: int) -> list[History]:
        result = await self.session.execute(
            select(HistoryModel).where(HistoryModel.user_id == user_id)
        )
        history_models = result.scalars().all()
        return [model.to_entity() for model in history_models]
    
    async def remove_history(self, history_id: int) -> None:
        result = await self.session.execute(
            select(HistoryModel).where(HistoryModel.id == history_id)
        )
        history_model = result.scalar_one_or_none()
        if history_model:
            await self.session.delete(history_model)
            await self.session.commit()
        else:
            raise ValueError("History not found")