from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from blog.domain.entities.comment import Comment
from blog.domain.repositories.comment_repository import CommentRepository
from blog.infra.models.comment_model import CommentModel

class SQLAlchemyCommentRepository(CommentRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_movie_id(self, movie_id: str) -> list[Comment]:
        result = await self._session.execute(
            select(CommentModel).where(CommentModel.movieId == movie_id)
        )
        return [comment.to_entity() for comment in result.scalars().all()]

    async def create(self, comment: Comment) -> None:
        comment_model = CommentModel.from_entity(comment)
        self._session.add(comment_model)
        await self._session.commit()

    async def update(self, comment: Comment) -> None:
        comment_model = CommentModel.from_entity(comment)
        await self._session.merge(comment_model)
        await self._session.commit()

    async def delete(self, comment_id: str) -> None:
        await self._session.execute(
            delete(CommentModel).where(CommentModel.id == comment_id)
        )
        await self._session.commit()