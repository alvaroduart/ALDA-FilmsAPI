from blog.domain.entities.movie import Movie
from blog.domain.repositories.movie_repository import MovieRepository


class InMemoryMovieRepository(MovieRepository):
    def __init__(self):
        self._movies = {}

    def get_all(self) -> list[Movie]:
        return list(self._movies.values())

    def get_by_id(self, movie_id: str) -> Movie:
        movie = self._movies.get(movie_id)
        if not movie:
            raise ValueError(f"Movie with id {movie_id} not found")
        return movie
    
    def search(self, query: str) -> list[Movie]:
        query_lower = query.lower()
        return [movie for movie in self._movies.values() 
                if query_lower in movie.title.lower() or 
                (movie.description and query_lower in movie.description.lower())]
    
    def create(self, movie: Movie) -> None:
        if movie.id in self._movies:
            raise ValueError(f"Movie with id {movie.id} already exists")
        self._movies[movie.id] = movie
    
   
