from blog.domain.entities.history import History
from blog.domain.repositories.history_repository import HistoryRepository


class InMemoryHistoryRepository(HistoryRepository):
    def __init__(self):
        self._history = []

    def get_by_user_id(self, user_id: str) -> list[History]:
        return [history for history in self._history 
                if history.userId == user_id]

    def add_to_history(self, history: History) -> None:
        if not self.is_in_history(history.userId, history.movieId):
            self._history.append(history)

    def remove_from_history(self, user_id: str, movie_id: str) -> None:
        self._history = [history for history in self._history 
                        if not (history.userId == user_id and history.movieId == movie_id)]

    def is_in_history(self, user_id: str, movie_id: str) -> bool:
        return any(history.userId == user_id and history.movieId == movie_id 
                  for history in self._history)
