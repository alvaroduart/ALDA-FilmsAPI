from blog.domain.entities.movie import Movie
from blog.domain.repositories.movie_repository import MovieRepository


class CreateMovieUseCase:
    def __init__(self, repository: MovieRepository):
        self.repository = repository

    async def execute(self, movie: Movie) -> None:
        await self.repository.create(movie)
