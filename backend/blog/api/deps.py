from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import AsyncGenerator, Any

from blog.api.settings import settings
from blog.domain.entities.user import User

from blog.infra.repositories.sqlalchemy.sqlalchemy_user_repository import SQLAlchemyUserRepository
from blog.infra.repositories.sqlalchemy.sqlalchemy_movie_repository import SQLAlchemyMovieRepository
from blog.infra.repositories.sqlalchemy.sqlalchemy_comment_repository import SQLAlchemyCommentRepository
from blog.infra.repositories.sqlalchemy.sqlalchemy_favorite_repository import SQLAlchemyFavoriteRepository
from blog.infra.repositories.sqlalchemy.sqlalchemy_history_repository import SQLAlchemyHistoryRepository
from blog.infra.repositories.sqlalchemy.sqlalchemy_contact_repository import SQLAlchemyContactRepository

from blog.infra.database import async_session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_user_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)


async def get_movie_repository(
    db: AsyncSession = Depends(get_db_session),
) -> Any:  # Usando Any até a classe ser totalmente implementada
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
) -> SQLAlchemyHistoryRepository:  # Agora pode usar diretamente
    return SQLAlchemyHistoryRepository(db)


async def get_contact_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyContactRepository:
    return SQLAlchemyContactRepository(db)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: SQLAlchemyUserRepository = Depends(get_user_repository),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not isinstance(user_id, str):
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_repo.get_current_user(user_id)
    if user is None:
        raise credentials_exception
    return user
