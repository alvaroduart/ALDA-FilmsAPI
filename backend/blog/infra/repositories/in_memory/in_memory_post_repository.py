from blog.domain.repositories.post_repository import PostRepository
from blog.domain.entities.post import Post
from typing import List, Optional
import pytest


class InMemoryPostRepository(PostRepository):
    def __init__(self):
        self._posts = {}

    @pytest.mark.asyncio
    async def get_all(self) -> List[Post]:
        return list(self._posts.values())

    @pytest.mark.asyncio
    async def get_by_id(self, post_id: str) -> Optional[Post]:
        return self._posts.get(post_id)

    @pytest.mark.asyncio
    async def create(self, post: Post) -> Optional[Post]:
        self._posts[post.id] = post
        return post

    @pytest.mark.asyncio
    async def update(self, post: Post) -> Optional[Post]:
        if post.id in self._posts:
            self._posts[post.id] = post
            return post
        return None

    @pytest.mark.asyncio
    async def delete(self, post_id: str) -> None:
        self._posts.pop(post_id, None)
