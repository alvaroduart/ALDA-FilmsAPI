from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from typing import List
from datetime import datetime
from blog.api.schemas.comment_schema import (
    AddCommentInput,
    UpdateCommentInput,
    DeleteCommentInput,
    CommentOutput,
)
from blog.domain.entities.comment import Comment
from blog.domain.repositories.comment_repository import CommentRepository
from blog.api.deps import get_comment_repository, get_current_user
from blog.usecases.comment.get_comments_by_movie import GetCommentsByMovieUseCase
from blog.usecases.comment.update_comment import UpdateCommentUseCase
from blog.usecases.comment.delete_comment import DeleteCommentUseCase
from blog.usecases.comment.create_comment import AddCommentUseCase

import uuid
from blog.domain.entities.user import User

security = HTTPBearer()
router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentOutput)
async def create_comment(
    data: AddCommentInput,
    user: User = Depends(get_current_user),  # Uncomment if you want to use User entity
    credentials=Depends(security),
    repo: CommentRepository = Depends(get_comment_repository),
):
    comment = Comment(
        id=str(uuid.uuid4()),
        movieId=data.movieId,
        userId=user.id,
        userName=user.name,
        content=data.content,
        createdAt=datetime.now(),
    )
    usecase = AddCommentUseCase(repo)
    created = await usecase.execute(comment)
    return CommentOutput.from_entity(created)


@router.put("/", response_model=CommentOutput)
async def update_comment(
    data: UpdateCommentInput,
    credentials=Depends(security),
    user: User = Depends(get_current_user),  # Uncomment if you want to use User entity
    repo: CommentRepository = Depends(get_comment_repository),
):
    comment = Comment(
        id=data.id,
        movieId=data.movieId or "",
        userId=user.id or "",
        userName=user.name or "",
        content=data.content or "",
        createdAt=datetime.now(),
    )
    usecase = UpdateCommentUseCase(repo)
    result = await usecase.execute(comment)
    return CommentOutput.from_entity(result)


@router.delete("/", status_code=204)
async def delete_comment(
    data: DeleteCommentInput,
    credentials=Depends(security),
    repo: CommentRepository = Depends(get_comment_repository),
):
    usecase = DeleteCommentUseCase(repo)
    await usecase.execute(data.id)


@router.get("/movie/{movie_id}", response_model=List[CommentOutput])
async def get_comments_by_movie(
    movie_id: str, repo: CommentRepository = Depends(get_comment_repository)
):
    usecase = GetCommentsByMovieUseCase(repo)
    comments = await usecase.execute(movie_id)
    return [CommentOutput.from_entity(c) for c in comments]
