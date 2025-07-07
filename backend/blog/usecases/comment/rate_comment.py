from blog.domain.entities.comment import Comment
from blog.domain.repositories.comment_repository import CommentRepository

class RateCommentUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    def execute(self, comment_id: str, rating: int) -> None:
        if not comment_id:
            raise ValueError("Comment ID is required for rating")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        comment = self.repository.get_by_id(comment_id)
        if not comment:
            raise ValueError("Comment not found")

        comment.rating = rating
        self.repository.update(comment)

