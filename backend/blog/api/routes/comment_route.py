from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from blog.usecases.comment import (
    UpdateCommentUseCase,    
    AddCommentUseCase,
    GetCommentsByMovieIdUseCase,    
    DeleteCommentUseCase,
)
from blog.domain.entities.comment import Comment
from blog.domain.entities.user import User
import uuid
from blog.api.schemas.comment_schema import AddCommentInput, CommentOutput
from blog.domain.repositories.comment_repository import CommentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from blog.api.deps import (
    get_db_session,
    get_user_repository,
    get_comment_repository,
    get_current_user,
)
from blog.infra.repositories.sqlalchemy.sqlalchemy_comment_repository import (
    SQLAlchemyCommentRepository,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
router = APIRouter()

@router.get("/{movie_id}", response_model=List[CommentOutput])
async def get_comments_by_movie(
    movie_id: str,
    db: AsyncSession = Depends(get_db_session),
    comment_repository: CommentRepository = Depends(SQLAlchemyCommentRepository),
):
    use_case = GetCommentsByMovieIdUseCase(comment_repository)
    comments = await use_case.execute(movie_id)
    return [CommentOutput.from_entity(comment) for comment in comments]

@router.post("/", response_model=CommentOutput)
async def add_comment(
    comment_input: AddCommentInput,
    db: AsyncSession = Depends(get_db_session),
    comment_repository: CommentRepository = Depends(SQLAlchemyCommentRepository),
    current_user: User = Depends(get_current_user),
):
    comment = Comment(
        id=str(uuid.uuid4()),
        movieId=comment_input.movieId,
        userId=current_user.id,
        userName=current_user.name,
        content=comment_input.content,
    )
    use_case = AddCommentUseCase(comment_repository)
    await use_case.execute(comment)
    return CommentOutput.from_entity(comment)

@router.put("/{comment_id}", response_model=CommentOutput)
async def update_comment(
    comment_id: str,
    comment_input: AddCommentInput,
    db: AsyncSession = Depends(get_db_session),
    comment_repository: CommentRepository = Depends(SQLAlchemyCommentRepository),
    current_user: User = Depends(get_current_user),
):
    comment = Comment(
        id=comment_id,
        movieId=comment_input.movieId,
        userId=current_user.id,
        userName=current_user.name,
        content=comment_input.content,
    )
    use_case = UpdateCommentUseCase(comment_repository)
    updated_comment = await use_case.execute(comment)
    return CommentOutput.from_entity(updated_comment)

@router.delete("/{comment_id}", response_model=None)
async def delete_comment(
    comment_id: str,
    db: AsyncSession = Depends(get_db_session),
    comment_repository: CommentRepository = Depends(SQLAlchemyCommentRepository),
    current_user: User = Depends(get_current_user),
):
    use_case = DeleteCommentUseCase(comment_repository)
    await use_case.execute(comment_id, current_user.id)
    return {"message": "Comment deleted successfully"}

@router.get("/user/{user_id}", response_model=List[CommentOutput])
async def get_comments_by_user(
    user_id: str,
    db: AsyncSession = Depends(get_db_session),
    comment_repository: CommentRepository = Depends(SQLAlchemyCommentRepository),
):
    use_case = GetCommentsByMovieIdUseCase(comment_repository)
    comments = await use_case.execute(user_id)
    return [CommentOutput.from_entity(comment) for comment in comments]

@router.get("/user/current/{movie_id}", response_model=List[CommentOutput])
async def get_current_user_comments_by_movie(
    movie_id: str,
    db: AsyncSession = Depends(get_db_session),
    comment_repository: CommentRepository = Depends(SQLAlchemyCommentRepository),
    current_user: User = Depends(get_current_user),
):
    use_case = GetCommentsByMovieIdUseCase(comment_repository)
    comments = await use_case.execute(movie_id, current_user.id)
    return [CommentOutput.from_entity(comment) for comment in comments]

