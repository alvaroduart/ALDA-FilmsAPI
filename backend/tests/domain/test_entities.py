import pytest
from datetime import datetime, timedelta
from blog.domain.entities.user import User
from blog.domain.entities.comment import Comment
from blog.domain.entities.favorite import Favorite
from blog.domain.entities.history import History
from blog.domain.entities.movie import Movie
from blog.domain.entities.contact import Contact
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password


def test_comment_creation():
    c = Comment(
        id="c1",
        movieId="m1",
        userId="u1",
        userName="John",
        content="Great movie!",
        createdAt=datetime.now(),
    )
    assert c.id == "c1"
    assert c.movieId == "m1"
    assert c.userId == "u1"
    assert c.userName == "John"
    assert c.content == "Great movie!"
    assert isinstance(c.createdAt, datetime)


def test_contact_creation():
    contact = Contact(
        id="contact1",
        name="Alice",
        email="alice@example.com",
        message="What time does the movie start?",
    )
    assert contact.id == "contact1"
    assert contact.name == "Alice"
    assert contact.email == "alice@example.com"
    assert contact.message == "What time does the movie start?"


def test_favorite_creation():
    fav = Favorite(userId="u123", movieId="m123")
    assert fav.userId == "u123"
    assert fav.movieId == "m123"


def test_history_creation_minimal():
    history = History(userId="userX", movieId="movieX")
    assert history.userId == "userX"
    assert history.movieId == "movieX"
    # não testa timestamp porque não existe na entidade


def test_movie_creation_with_defaults():
    movie = Movie(id="mov1", title="Inception", image="inception.jpg", rating=9.0)
    assert movie.id == "mov1"
    assert movie.title == "Inception"
    assert movie.image == "inception.jpg"
    assert movie.rating == 9.0
    assert movie.description in (None, "")
    assert movie.genre in (None, "")
    assert movie.duration in (None, "")
    assert movie.director in (None, "")


def test_user_creation_with_email_password():
    email = Email("user@example.com")
    password = Password("StrongPass123!")
    user = User(id="user1", name="User One", email=email, password=password)
    assert user.id == "user1"
    assert user.name == "User One"
    assert isinstance(user.email, Email)
    assert user.email.value() == "user@example.com"
    assert isinstance(user.password, Password)
