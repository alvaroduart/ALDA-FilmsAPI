from blog.domain.entities.comment import Comment
from blog.domain.repositories.comment_repository import CommentRepository


class InMemoryCommentRepository(CommentRepository):
    def __init__(self):
        self._comments = {}

    def get_by_movie_id(self, movie_id: str) -> list[Comment]:
        return [comment for comment in self._comments.values() 
                if comment.movieId == movie_id] 

    def create(self, comment: Comment) -> None:
        self._comments[comment.id] = comment

    def update(self, comment: Comment) -> None:
        if comment.id not in self._comments:
            raise ValueError(f"Comment with id {comment.id} not found")
        self._comments[comment.id] = comment

    def delete(self, comment_id: str) -> None:
        if comment_id not in self._comments:
            raise ValueError(f"Comment with id {comment_id} not found")
        del self._comments[comment_id]
