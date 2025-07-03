from abc import ABC, abstractmethod
from blog.domain.entities.post import Post
from typing import Optional


class PostRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Post]:
        pass

    @abstractmethod
    def get_by_id(self, post_id: str) -> Optional[Post]: ...

    @abstractmethod
    def create(self, post: Post) -> Optional[Post]: ...

    @abstractmethod
    def update(self, post: Post) -> Optional[Post]: ...

    @abstractmethod
    def delete(self, post_id: str) -> None:
        pass
