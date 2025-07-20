from blog.domain.entities.favorite import Favorite
from blog.domain.repositories.favorite_repository import FavoriteRepository


class AddToFavoritesUseCase:
    def __init__(self, repository: FavoriteRepository):
        self.repository = repository

    async def execute(self, user_id: str, movie_id: str) -> Favorite | None:
        favorite = Favorite(user_id, movie_id)
        return await self.repository.add_favorite(favorite)
