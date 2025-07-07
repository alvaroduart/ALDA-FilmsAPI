import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from blog.domain.entities.user import User
import uuid
from datetime import datetime
from blog.infra.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(sa.String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(sa.String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow)

    def to_entity(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            email=self.email,
            password=self.password,
            favoriteMovies=[],
            watchedMovies=[],
            createdAt=self.createdAt
        )
    
    favorites = relationship("FavoriteModel", back_populates="user")
    watchedMovies = relationship("HistoryModel", back_populates="user")
    
    @classmethod
    def from_entity(cls, user: User) -> "UserModel":
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            favoriteMovies=[],
            watchedMovies=[],
            createdAt=user.createdAt
        )