from blog.domain.entities.comment import Comment
from blog.domain.repositories.comment_repository import CommentRepository


class AddCommentUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    def execute(self, comment: Comment) -> Comment:
        self.repository.create(comment)
        return comment
    
    def rate_comment(self, comment_id: str, rating: int) -> None:
        self.repository.rate(comment_id, rating)

