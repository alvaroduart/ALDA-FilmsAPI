from abc import ABC, abstractmethod
from blog.domain.entities.history import History


class HistoryRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> list[History]:
        pass

    @abstractmethod
    async def add_to_history(self, history: History) -> None:
        pass

    @abstractmethod
    async def remove_from_history(self, user_id: str, movie_id: str) -> None:
        pass

    @abstractmethod
    async def is_in_history(self, user_id: str, movie_id: str) -> bool:
        pass
