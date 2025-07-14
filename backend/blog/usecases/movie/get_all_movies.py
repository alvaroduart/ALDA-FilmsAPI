from blog.domain.entities.movie import Movie
from blog.domain.repositories.movie_repository import MovieRepository
from typing import List


class GetAllMoviesUseCase:
    def __init__(self, repository: MovieRepository):
        self.repository = repository

    async def execute(self) -> List[Movie]:
        return await self.repository.get_all()
