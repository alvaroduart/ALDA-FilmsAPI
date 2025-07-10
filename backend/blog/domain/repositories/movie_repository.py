from abc import ABC, abstractmethod
from blog.domain.entities.movie import Movie

class MovieRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Movie]:
        pass

    @abstractmethod
    async def get_by_id(self, movie_id: str) -> Movie:
        pass
    
    @abstractmethod
    async def search(self, query: str) -> list[Movie]:
        pass

    @abstractmethod
    async def create(self, movie: Movie) -> None:
        pass
    
 

