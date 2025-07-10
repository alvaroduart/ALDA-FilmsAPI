from blog.domain.repositories.comment_repository import CommentRepository


class DeleteCommentUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def execute(self, comment_id: str) -> None:
       await self.repository.delete(comment_id)

