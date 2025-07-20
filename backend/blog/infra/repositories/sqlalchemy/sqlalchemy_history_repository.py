from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from blog.domain.entities.history import History
from blog.domain.repositories.history_repository import HistoryRepository
from blog.infra.models.history_model import HistoryModel


class SQLAlchemyHistoryRepository(HistoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_to_history(self, history: History) -> History:
        history_model = HistoryModel.from_entity(history)
        if await self.is_in_history(history.userId, history.movieId):
            raise ValueError("History already exists.")
        self.session.add(history_model)
        await self.session.commit()

        history_sel = await self.session.execute(
            select(HistoryModel)
            .options(joinedload(HistoryModel.movie))
            .where(
                HistoryModel.userId == history.userId,
                HistoryModel.movieId == history.movieId,
            )
        )
        history_entity = history_sel.scalar_one_or_none()
        if not history_entity:
            raise ValueError("History not found after adding")
        print(history_entity.to_entity().userId)
        return history_entity.to_entity()

    async def get_by_user_id(self, user_id: str) -> list[History]:
        result = await self.session.execute(
            select(HistoryModel)
            .options(joinedload(HistoryModel.movie))
            .where(HistoryModel.userId == user_id)
        )
        history_models = result.scalars().all()
        return [model.to_entity() for model in history_models]

    async def remove_from_history(self, user_id: str, movie_id: str) -> None:
        result = await self.session.execute(
            select(HistoryModel).where(
                HistoryModel.userId == user_id, HistoryModel.movieId == movie_id
            )
        )
        history_model = result.scalar_one_or_none()
        if history_model:
            await self.session.delete(history_model)
            await self.session.commit()
        else:
            raise ValueError("History not found")

    async def is_in_history(self, user_id: str, movie_id: str) -> bool:
        result = await self.session.execute(
            select(HistoryModel)
            .options(joinedload(HistoryModel.movie))
            .where(HistoryModel.userId == user_id, HistoryModel.movieId == movie_id)
        )
        return result.scalar_one_or_none() is not None
