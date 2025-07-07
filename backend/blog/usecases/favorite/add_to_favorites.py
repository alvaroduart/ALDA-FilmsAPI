from blog.domain.entities.favorite import Favorite
from blog.domain.repositories.favorite_repository import FavoriteRepository


class AddToFavoritesUseCase:
    def __init__(self, repository: FavoriteRepository):
        self.repository = repository

    def execute(self, user_id: str, movie_id: str) -> None:
        if not self.repository.is_favorite(user_id, movie_id):
            favorite = Favorite(user_id, movie_id)
            self.repository.add_favorite(favorite)

