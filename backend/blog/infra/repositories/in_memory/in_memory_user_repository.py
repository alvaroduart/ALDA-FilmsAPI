from blog.domain.entities.user import User
from blog.domain.repositories.user_repository import UserRepository
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = {}

    def create(self, user: User) -> None:
        self._users[user.id] = user

    def get_by_id(self, user_id: str) -> User:
        if user_id in self._users:
            return self._users[user_id]
        raise ValueError(f"User with id {user_id} not found")

    def get_by_email(self, email: Email) -> User | None:
        for user in self._users.values():
            if user.email.value() == email.value():
                return user
        return None

    def login(self, email: Email, password: Password) -> User:
        for user in self._users.values():
            if user.email == email and user.password == password:
                return user
        raise ValueError("Invalid email or password")

    def logout(self, user_id: str) -> None:
        if user_id not in self._users:
            raise ValueError(f"User with id {user_id} not found")

    def forgot_password(self, email: Email) -> None:
        if not self.get_by_email(email):
            raise ValueError(f"User with email {email.value()} not found")