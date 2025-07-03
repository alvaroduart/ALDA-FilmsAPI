from blog.domain.repositories.post_repository import PostRepository
from blog.domain.entities.post import Post
from typing import List


class GetAllPostsUseCase:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def execute(self) -> List[Post]:
        return await self.repository.get_all()
