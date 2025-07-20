from abc import ABC, abstractmethod
from blog.domain.entities.rating import Rating


class RatingRepository(ABC):
    @abstractmethod
    async def add_rating(self, rating: Rating) -> Rating:
        """Add a new rating to the repository."""
        pass

    @abstractmethod
    async def update_rating(self, rating: Rating) -> Rating:
        """Update an existing rating in the repository."""
        pass

    @abstractmethod
    async def is_rated(self, user_id: str, movie_id: str) -> bool:
        """Check if a user has already rated a movie."""
        pass

    @abstractmethod
    async def get_rating(self, user_id: str, movie_id: str) -> Rating | None:
        """Retrieve a user's rating for a specific movie."""
        pass
