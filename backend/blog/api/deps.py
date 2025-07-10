# Instâncias SQLAlchemy
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from blog.api.settings import settings
from blog.domain.repositories.user_repository import UserRepository
from blog.domain.repositories.movie_repository import MovieRepository
from blog.domain.repositories.comment_repository import CommentRepository
from blog.domain.repositories.favorite_repository import FavoriteRepository
from blog.domain.repositories.history_repository import HistoryRepository
from blog.domain.repositories.contact_repository import ContactRepository

from blog.infra.repositories.sqlalchemy.sqlalchemy_user_repository import SQLAlchemyUserRepository
from blog.infra.repositories.sqlalchemy.sqlalchemy_movie_repository import SQLAlchemyMovieRepository
from blog.infra.repositories.sqlalchemy.sqlalchemy_comment_repository import SQLAlchemyCommentRepository
from blog.infra.repositories.sqlalchemy.sqlalchemy_favorite_repository import SQLAlchemyFavoriteRepository
from blog.infra.repositories.sqlalchemy.sqlalchemy_history_repository import SQLAlchemyHistoryRepository
from blog.infra.repositories.sqlalchemy.sqlalchemy_contact_repository import SQLAlchemyContactRepository
from sqlalchemy.ext.asyncio import AsyncSession
from blog.infra.database import async_session
from blog.domain.entities.user import User


async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_user_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)


async def get_movie_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyMovieRepository:
    return SQLAlchemyMovieRepository(db)


async def get_comment_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyCommentRepository:
    return SQLAlchemyCommentRepository(db)


async def get_favorite_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyFavoriteRepository:
    return SQLAlchemyFavoriteRepository(db)


async def get_history_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyHistoryRepository:
    return SQLAlchemyHistoryRepository(db)


async def get_contact_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyContactRepository:
    return SQLAlchemyContactRepository(db)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_repo.get_current_user(user_id)
    if user is None:
        raise credentials_exception
    return user
