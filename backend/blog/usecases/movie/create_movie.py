from blog.domain.entities.movie import Movie
from blog.domain.repositories.movie_repository import MovieRepository


class CreateMovieUseCase:
    def __init__(self, repository: MovieRepository):
        self.repository = repository

    def execute(self, movie: Movie) -> None:
        self.repository.create(movie)