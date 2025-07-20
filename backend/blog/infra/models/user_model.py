import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from blog.domain.entities.user import User
import uuid
from blog.infra.database import Base
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    username: Mapped[str] = mapped_column(sa.String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(sa.String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String(255), nullable=False)

    favorites = relationship(
        "FavoriteModel", back_populates="user", cascade="all, delete-orphan"
    )
    watchedMovies = relationship(
        "HistoryModel", back_populates="user", cascade="all, delete-orphan"
    )
    comments = relationship(
        "CommentModel", back_populates="user", cascade="all, delete-orphan"
    )
    ratings = relationship(
        "RatingModel", back_populates="user", cascade="all, delete-orphan"
    )

    def to_entity(self) -> User:
        return User(
            id=self.id,
            name=self.username,
            email=Email(self.email),
            password=Password(self.password),
        )

    @classmethod
    def from_entity(cls, user: User) -> "UserModel":
        return cls(
            id=user.id,
            username=user.name,
            email=str(user.email),
            password=str(user.password),
        )
