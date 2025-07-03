from fastapi import APIRouter, HTTPException, Depends
from blog.usecases.post.create_post import CreatePostUseCase
from blog.usecases.post.delete_post import DeletePostUseCase
from blog.usecases.post.get_all_posts import GetAllPostsUseCase
from blog.usecases.post.get_post_by_id import GetPostByIdUseCase
from blog.usecases.post.update_post import UpdatePostUseCase
from blog.domain.entities.post import Post
from blog.domain.entities.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from blog.api.deps import (
    get_user_repository,
    get_current_user,
    get_db_session,
    get_post_repository,
)
from typing import List
from blog.domain.repositories.post_repository import PostRepository

from blog.api.schemas.post_schema import PostCreateInput

import uuid
from blog.api.schemas.post_schema import PostOutput, PostCreateInput, PostUpdateInput
from blog.infra.repositories.sqlalchemy.sqlalchemy_post_repository import (
    SQLAlchemyPostRepository,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
router = APIRouter()


@router.get("/", response_model=List[PostOutput])
async def get_all_posts(
    post_repo: PostRepository = Depends(get_post_repository),
):
    usecase = GetAllPostsUseCase(post_repo)
    posts = await usecase.execute()
    return posts


@router.get("/{post_id}", response_model=PostOutput)
async def get_post_by_id(
    post_id: str,
    post_repo: PostRepository = Depends(get_post_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    usecase = GetPostByIdUseCase(post_repo)
    post = await usecase.execute(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", response_model=PostOutput)
async def create_post(
    data: PostCreateInput,
    db: AsyncSession = Depends(get_db_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: str = Depends(get_current_user),
    post_repo: PostRepository = Depends(get_post_repository),
):
    usecase = CreatePostUseCase(post_repo)
    if data.date.tzinfo is not None:
        data.date = data.date.replace(tzinfo=None)
    post = Post(
        id=str(uuid.uuid4()),
        title=data.title,
        description=data.description,
        content=data.content,
        user_id=user.id,
        date=data.date,
    )
    created_post = await usecase.execute(post)
    return created_post


@router.put("/{post_id}", response_model=PostOutput)
async def update_post(
    post_id: str,
    data: PostUpdateInput,
    post_repo: PostRepository = Depends(get_post_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    usecase_get = GetPostByIdUseCase(post_repo)
    existing_post = await usecase_get.execute(post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    updated_post = Post(
        id=post_id,
        title=data.title,
        description=data.description,
        content=data.content,
        user_id=existing_post.user_id,
        date=existing_post.date,
    )
    usecase_update = UpdatePostUseCase(post_repo)
    result = await usecase_update.execute(updated_post)
    return result


@router.delete("/{post_id}")
async def delete_post(
    post_id: str,
    post_repo: PostRepository = Depends(get_post_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    usecase = DeletePostUseCase(post_repo)
    success = await usecase.execute(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
