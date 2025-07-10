from blog.domain.entities.history import History
from blog.domain.repositories.history_repository import HistoryRepository


class AddToHistoryUseCase:
    def __init__(self, repository: HistoryRepository):
        self.repository = repository

    async def execute(self, user_id: str, movie_id: str) -> None:
        if not self.repository.is_in_history(user_id, movie_id):
            history = History(user_id, movie_id)
            await self.repository.add_to_history(history)

