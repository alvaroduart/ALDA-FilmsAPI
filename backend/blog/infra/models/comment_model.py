import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from blog.domain.entities.comment import Comment
import uuid
from datetime import datetime
from blog.infra.database import Base

class CommentModel(Base):
    __tablename__ = "comments"

    id: Mapped[str] = mapped_column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    movieId: Mapped[str] = mapped_column(sa.String(36), nullable=False)
    userId: Mapped[str] = mapped_column(sa.String(36), nullable=False)
    userName: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow)

    def to_entity(self) -> Comment:
        return Comment(
            id=self.id,
            movieId=self.movieId,
            userId=self.userId,
            userName=self.userName,
            content=self.content,
            createdAt=self.createdAt
        )
    
    movie = relationship("MovieModel", back_populates="comments")
    user = relationship("UserModel", back_populates="comments")

    @classmethod
    def from_entity(cls, comment: Comment) -> "CommentModel":
        return cls(
            id=comment.id,
            movieId=comment.movieId,
            userId=comment.userId,
            userName=comment.userName,
            content=comment.content,
            createdAt=comment.createdAt
        )
    
  