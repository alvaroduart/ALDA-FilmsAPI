from blog.domain.entities.history import History
from blog.domain.repositories.history_repository import HistoryRepository
import pytest

class InMemoryHistoryRepository(HistoryRepository):
    def __init__(self):
        self._history = []

    @pytest.mark.asyncio
    async def get_by_user_id(self, user_id: str) -> list[History]:
        return [history for history in self._history 
                if history.userId == user_id]

    @pytest.mark.asyncio
    async def add_to_history(self, history: History) -> None:
        if not self.is_in_history(history.userId, history.movieId):
            self._history.append(history)

    @pytest.mark.asyncio
    async def remove_from_history(self, user_id: str, movie_id: str) -> None:
        self._history = [history for history in self._history 
                        if not (history.userId == user_id and history.movieId == movie_id)]

    @pytest.mark.asyncio
    async def is_in_history(self, user_id: str, movie_id: str) -> bool:
        return any(history.userId == user_id and history.movieId == movie_id 
                  for history in self._history)
