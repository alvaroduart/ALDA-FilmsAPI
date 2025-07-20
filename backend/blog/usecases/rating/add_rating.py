from blog.domain.repositories.rating_repository import RatingRepository
from blog.domain.entities.rating import Rating


class AddRatingUseCase:
    def __init__(self, repository: RatingRepository):
        self.repository = repository

    async def execute(self, user_id: str, movie_id: str, rating_value: int) -> Rating:
        rating = Rating(userId=user_id, movieId=movie_id, rating=rating_value)
        return await self.repository.add_rating(rating)
