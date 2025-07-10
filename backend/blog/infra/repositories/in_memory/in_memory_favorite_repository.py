from blog.domain.entities.favorite import Favorite
from blog.domain.repositories.favorite_repository import FavoriteRepository
import pytest

class InMemoryFavoriteRepository(FavoriteRepository):
    def __init__(self):
        self._favorites = []

    @pytest.mark.asyncio
    async def get_by_user_id(self, user_id: str) -> list[Favorite]:
        return [favorite for favorite in self._favorites 
                if favorite.userId == user_id]

    @pytest.mark.asyncio
    async def add_favorite(self, favorite: Favorite) -> None:
        if not self.is_favorite(favorite.userId, favorite.movieId):
            self._favorites.append(favorite)

    @pytest.mark.asyncio
    async def remove_favorite(self, user_id: str, movie_id: str) -> None:
        self._favorites = [favorite for favorite in self._favorites 
                          if not (favorite.userId == user_id and favorite.movieId == movie_id)]
    
    @pytest.mark.asyncio
    async def is_favorite(self, user_id: str, movie_id: str) -> bool:
        return any(favorite.userId == user_id and favorite.movieId == movie_id 
                  for favorite in self._favorites)
