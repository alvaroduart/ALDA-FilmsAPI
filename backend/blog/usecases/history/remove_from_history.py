from blog.domain.repositories.history_repository import HistoryRepository


class RemoveFromHistoryUseCase:
    def __init__(self, repository: HistoryRepository):
        self.repository = repository

    async def execute(self, user_id: str, movie_id: str) -> None:
        await self.repository.remove_from_history(user_id, movie_id)
