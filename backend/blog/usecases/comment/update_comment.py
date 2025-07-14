from blog.domain.entities.comment import Comment
from blog.domain.repositories.comment_repository import CommentRepository


class UpdateCommentUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def execute(self, comment: Comment) -> None:
        if not comment.id:
            raise ValueError("Comment ID is required for update")
        await self.repository.update(comment)
