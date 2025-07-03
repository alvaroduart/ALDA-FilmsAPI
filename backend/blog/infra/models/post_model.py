import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from blog.domain.entities.post import Post
import uuid
from datetime import datetime
from blog.infra.database import Base


class PostModel(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(
        sa.String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    description: Mapped[str] = mapped_column(sa.String, nullable=False)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    user_id: Mapped[str] = mapped_column(sa.String, sa.ForeignKey("users.id"))
    date: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.now())

    user = relationship("UserModel", back_populates="posts")
    comments = relationship(
        "CommentModel", back_populates="post", cascade="all, delete"
    )

    @classmethod
    def from_entity(cls, entity: Post) -> "PostModel":
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            content=entity.content,
            user_id=entity.user_id,
            date=entity.date,
        )

    def to_entity(self) -> Post:
        return Post(
            id=self.id,
            title=self.title,
            description=self.description,
            content=self.content,
            user_id=self.user_id,
            date=self.date,
        )
