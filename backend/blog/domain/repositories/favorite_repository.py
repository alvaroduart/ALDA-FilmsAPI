from abc import ABC, abstractmethod
from blog.domain.entities.favorite import Favorite

class FavoriteRepository(ABC):
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> list[Favorite]:
        pass

    @abstractmethod
    def add_favorite(self, favorite: Favorite) -> None:
        pass

    @abstractmethod
    def remove_favorite(self, user_id: str, movie_id: str) -> None:
        pass

    @abstractmethod
    def is_favorite(self, user_id: str, movie_id: str) -> bool:
        pass

