from blog.domain.entities.history import History
from blog.domain.repositories.history_repository import HistoryRepository


class AddToHistoryUseCase:
    def __init__(self, repository: HistoryRepository):
        self.repository = repository

    async def execute(self, user_id: str, movie_id: str) -> History | None:
        return await self.repository.add_to_history(
            history=History(userId=user_id, movieId=movie_id)
        )
