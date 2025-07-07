from blog.domain.entities.favorite import Favorite
from blog.domain.repositories.favorite_repository import FavoriteRepository
from typing import List


class GetUserFavoritesUseCase:
    def __init__(self, repository: FavoriteRepository):
        self.repository = repository

    def execute(self, user_id: str) -> List[Favorite]:
        return self.repository.get_by_user_id(user_id)

