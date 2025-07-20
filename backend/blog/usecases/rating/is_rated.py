from blog.domain.repositories.rating_repository import RatingRepository


class IsRatedUseCase:
    def __init__(self, repository: RatingRepository):
        self.repository = repository

    async def execute(self, user_id: str, movie_id: str) -> bool:
        """Check if a user has already rated a movie."""
        return await self.repository.is_rated(user_id, movie_id)
