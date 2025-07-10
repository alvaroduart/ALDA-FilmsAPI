from abc import ABC, abstractmethod
from blog.domain.entities.comment import Comment

class CommentRepository(ABC):    
    
    @abstractmethod
    async def get_by_movie_id(self, movie_id: str) -> list[Comment]:
        pass
    
    @abstractmethod
    async def create(self, comment: Comment) -> None:
        pass

    @abstractmethod
    async def update(self, comment: Comment) -> None:
        pass

    @abstractmethod
    async def delete(self, comment_id: str) -> None: 
        pass

   

