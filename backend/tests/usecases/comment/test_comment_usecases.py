import pytest
from datetime import datetime
from blog.domain.entities.comment import Comment
from blog.infra.repositories.in_memory.in_memory_comment_repository import (
    InMemoryCommentRepository,
)
from blog.usecases.comment.get_comments_by_movie import GetCommentsByMovieUseCase
from blog.usecases.comment.create_comment import AddCommentUseCase
from blog.usecases.comment.update_comment import UpdateCommentUseCase
from blog.usecases.comment.delete_comment import DeleteCommentUseCase

pytestmark = pytest.mark.asyncio


async def test_add_comment():
    repo = InMemoryCommentRepository()
    add_use_case = AddCommentUseCase(repo)

    comment = Comment(
        id="1",
        userId="user1",
        userName="User One",
        movieId="movie1",
        content="Great movie!",
        createdAt=datetime.now(),
    )

    await add_use_case.execute(comment)

    stored_comments = await repo.get_by_movie_id("movie1")
    assert len(stored_comments) == 1
    assert stored_comments[0].id == "1"
    assert stored_comments[0].userId == "user1"
    assert stored_comments[0].userName == "User One"
    assert stored_comments[0].movieId == "movie1"
    assert stored_comments[0].content == "Great movie!"


async def test_get_comments_by_movie():
    repo = InMemoryCommentRepository()
    add_use_case = AddCommentUseCase(repo)

    comment1 = Comment(
        id="1",
        userId="user1",
        userName="User One",
        movieId="movie1",
        content="Great movie!",
        createdAt=datetime.now(),
    )
    comment2 = Comment(
        id="2",
        userId="user2",
        userName="User Two",
        movieId="movie1",
        content="I loved it!",
        createdAt=datetime.now(),
    )

    await add_use_case.execute(comment1)
    await add_use_case.execute(comment2)

    get_use_case = GetCommentsByMovieUseCase(repo)
    comments = await get_use_case.execute("movie1")

    assert len(comments) == 2
    assert comments[0].id == "1"
    assert comments[1].id == "2"


async def test_update_comment():
    repo = InMemoryCommentRepository()
    add_use_case = AddCommentUseCase(repo)

    original_comment = Comment(
        id="1",
        userId="user1",
        userName="User One",
        movieId="movie1",
        content="Great movie!",
        createdAt=datetime.now(),
    )

    await add_use_case.execute(original_comment)

    update_use_case = UpdateCommentUseCase(repo)

    updated_comment = Comment(
        id="1",
        userId="user1",
        userName="User One",
        movieId="movie1",
        content="Amazing movie!",
        createdAt=original_comment.createdAt,  # mantém data original
    )

    await update_use_case.execute(updated_comment)

    stored_comments = await repo.get_by_movie_id("movie1")
    assert len(stored_comments) == 1
    assert stored_comments[0].content == "Amazing movie!"


async def test_delete_comment():
    repo = InMemoryCommentRepository()
    add_use_case = AddCommentUseCase(repo)

    comment = Comment(
        id="1",
        userId="user1",
        userName="User One",
        movieId="movie1",
        content="Great movie!",
        createdAt=datetime.now(),
    )

    await add_use_case.execute(comment)

    delete_use_case = DeleteCommentUseCase(repo)
    await delete_use_case.execute("1")

    stored_comments = await repo.get_by_movie_id("movie1")
    assert len(stored_comments) == 0
