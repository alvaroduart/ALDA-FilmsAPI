from abc import ABC, abstractmethod
from blog.domain.entities.user import User
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password
from typing import Optional


class UserRepository(ABC):

    @abstractmethod
    async def get_by_id(self, user_id: str) -> User:
        pass

    @abstractmethod
    async def create(self, user: User) -> None:
        pass

    @abstractmethod
    async def login(self, email: Email, password: Password) -> User:
        pass

    @abstractmethod
    async def logout(self, user_id: str) -> None:
        pass

    @abstractmethod
    async def get_by_email(self, email: Email) -> Optional[User]:
        pass

    @abstractmethod
    async def get_current_user(self, user_id: str) -> User:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        pass
