from blog.domain.repositories.comment_repository import CommentRepository


class DeleteCommentUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def execute(self, comment_id: str) -> bool:
        await self.repository.delete_comment(comment_id)
        return True
