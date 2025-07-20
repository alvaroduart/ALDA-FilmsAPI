from blog.domain.repositories.rating_repository import RatingRepository
from blog.domain.entities.rating import Rating


class UpdateRatingUseCase:
    def __init__(self, repository: RatingRepository):
        self.repository = repository

    async def execute(self, rating: Rating) -> Rating:
        """Update an existing rating."""
        return await self.repository.update_rating(rating)
