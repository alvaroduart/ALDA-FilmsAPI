from blog.domain.entities.rating import Rating
from blog.domain.repositories.rating_repository import RatingRepository


class GetRatingUseCase:
    def __init__(self, repository: RatingRepository):
        self.repository = repository

    async def execute(self, user_id: str, movie_id: str) -> Rating | None:
        return await self.repository.get_rating(user_id, movie_id)
