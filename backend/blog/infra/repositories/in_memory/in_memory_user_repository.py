from blog.domain.entities.user import User
from blog.domain.repositories.user_repository import UserRepository
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password
import pytest


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.current_user = None
        self._users = {}

    @pytest.mark.asyncio
    async def create(self, user: User) -> None:
        self._users[user.id] = user
        self.current_user = user

    @pytest.mark.asyncio
    async def get_by_id(self, user_id: str) -> User:
        if user_id in self._users:
            return self._users[user_id]
        raise ValueError(f"User with id {user_id} not found")

    @pytest.mark.asyncio
    async def get_by_email(self, email: Email) -> User | None:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    @pytest.mark.asyncio
    async def login(self, email: Email, password: Password) -> User:
        for user in self._users.values():
            if user.email == email and password.verify(str(user.password)):
                self.current_user = user
                return user
        raise ValueError("Invalid email or password")

    @pytest.mark.asyncio
    async def logout(self) -> None:
        self.current_user = None

    @pytest.mark.asyncio
    async def forgot_password(self, email: Email) -> None:
        if not self.get_by_email(email):
            raise ValueError(f"User with email {email.value()} not found")

    async def get_by_username(self, username):
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    async def get_current_user(self):
        return self.current_user
