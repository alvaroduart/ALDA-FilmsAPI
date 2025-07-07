import pytest
from blog.domain.entities.comment import Comment
from blog.domain.repositories.comment_repository import CommentRepository
from blog.infra.repositories.in_memory.in_memory_comment_repository import InMemoryCommentRepository
from blog.usecases.comment.get_comments_by_movie import GetCommentsByMovieUseCase
from blog.usecases.comment.create_comment import AddCommentUseCase
from blog.usecases.comment.update_comment import UpdateCommentUseCase
from blog.usecases.comment.delete_comment import DeleteCommentUseCase

def test_add_comment():
    repo = InMemoryCommentRepository()
    add_use_case = AddCommentUseCase(repo)
    comment = Comment(id="1", userId="user1", userName="User One", movieId="movie1", content="Great movie!")
    add_use_case.execute(comment)   
    stored_comments = repo.get_by_movie_id("movie1")
    assert len(stored_comments) == 1
    assert stored_comments[0].id == "1"
    assert stored_comments[0].userId == "user1"
    assert stored_comments[0].userName == "User One"
    assert stored_comments[0].movieId == "movie1"
    assert stored_comments[0].content == "Great movie!"

def test_get_comments_by_movie():
    repo = InMemoryCommentRepository()
    add_use_case = AddCommentUseCase(repo)
    comment1 = Comment(id="1", userId="user1", userName="User One", movieId="movie1", content="Great movie!")
    comment2 = Comment(id="2", userId="user2", userName="User Two", movieId="movie1", content="I loved it!")
    add_use_case.execute(comment1)
    add_use_case.execute(comment2)

    get_use_case = GetCommentsByMovieUseCase(repo)
    comments = get_use_case.execute("movie1")

    assert len(comments) == 2
    assert comments[0].id == "1"
    assert comments[1].id == "2"

def test_update_comment():
    repo = InMemoryCommentRepository()
    add_use_case = AddCommentUseCase(repo)
    comment = Comment(id="1", userId="user1", userName="User One", movieId="movie1", content="Great movie!")
    add_use_case.execute(comment)

    update_use_case = UpdateCommentUseCase(repo)
    updated_comment = Comment(id="1", userId="user1", userName="User One", movieId="movie1", content="Amazing movie!")
    update_use_case.execute(updated_comment)

    stored_comments = repo.get_by_movie_id("movie1")
    assert len(stored_comments) == 1
    assert stored_comments[0].content == "Amazing movie!"

def test_delete_comment():
    repo = InMemoryCommentRepository()
    add_use_case = AddCommentUseCase(repo)
    comment = Comment(id="1", userId="user1", userName="User One", movieId="movie1", content="Great movie!")
    add_use_case.execute(comment)

    delete_use_case = DeleteCommentUseCase(repo)
    delete_use_case.execute("1")

    stored_comments = repo.get_by_movie_id("movie1")
    assert len(stored_comments) == 0

