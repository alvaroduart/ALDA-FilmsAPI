from abc import ABC, abstractmethod
from blog.domain.entities.movie import Movie

class MovieRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Movie]:
        pass

    @abstractmethod
    def get_by_id(self, movie_id: str) -> Movie:
        pass
    
    @abstractmethod
    def search(self, query: str) -> list[Movie]:
        pass

    @abstractmethod
    def create(self, movie: Movie) -> None:
        pass
    
 

