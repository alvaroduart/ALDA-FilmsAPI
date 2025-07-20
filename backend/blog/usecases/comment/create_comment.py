from blog.domain.entities.comment import Comment
from blog.domain.repositories.comment_repository import CommentRepository


class AddCommentUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def execute(self, comment: Comment) -> Comment | None:
        return await self.repository.create(comment)
