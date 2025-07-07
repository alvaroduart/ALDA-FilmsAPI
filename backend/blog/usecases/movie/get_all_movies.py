from blog.domain.entities.movie import Movie
from blog.domain.repositories.movie_repository import MovieRepository
from typing import List


class GetAllMoviesUseCase:
    def __init__(self, repository: MovieRepository):
        self.repository = repository

    def execute(self) -> List[Movie]:
        return self.repository.get_all()

