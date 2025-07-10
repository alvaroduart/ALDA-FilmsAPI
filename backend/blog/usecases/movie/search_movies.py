from blog.domain.entities.movie import Movie
from blog.domain.repositories.movie_repository import MovieRepository


class SearchMoviesUseCase:
    def __init__(self, repository: MovieRepository):
        self.repository = repository

    async def execute(self, query: str) -> list[Movie]:
        return await self.repository.search(query)

