from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from blog.domain.entities.post import Post
from blog.domain.repositories.post_repository import PostRepository
from blog.infra.models.post_model import PostModel


class SQLAlchemyPostRepository(PostRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> List[Post]:
        result = await self._session.execute(select(PostModel))
        return [post.to_entity() for post in result.scalars().all()]

    async def get_by_id(self, post_id: str) -> Optional[Post]:
        result = await self._session.execute(
            select(PostModel).where(PostModel.id == post_id)
        )
        post = result.scalar_one_or_none()
        return post.to_entity() if post else None

    async def create(self, post: Post) -> Post:
        db_post = PostModel.from_entity(post)
        self._session.add(db_post)
        await self._session.commit()
        await self._session.refresh(db_post)
        return db_post.to_entity()

    async def update(self, post: Post) -> Optional[Post]:
        stmt = (
            update(PostModel)
            .where(PostModel.id == post.id)
            .values(
                title=post.title,
                description=post.description,
                content=post.content,
                user_id=post.user_id,
                date=post.date,
            )
            .returning(PostModel)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        updated = result.scalar_one_or_none()
        return updated.to_entity() if updated else None

    async def delete(self, post_id: str) -> None:
        await self._session.execute(delete(PostModel).where(PostModel.id == post_id))
        await self._session.commit()
