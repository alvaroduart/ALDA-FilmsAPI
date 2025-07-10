from blog.domain.entities.movie import Movie
from blog.domain.repositories.movie_repository import MovieRepository


class GetMovieByIdUseCase:
    def __init__(self, repository: MovieRepository):
        self.repository = repository

    async def execute(self, movie_id: str) -> Movie:
        return await self.repository.get_by_id(movie_id)

