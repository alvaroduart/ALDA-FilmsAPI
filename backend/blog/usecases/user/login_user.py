from blog.domain.entities.user import User
from blog.domain.repositories.user_repository import UserRepository
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password


class LoginUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, email: Email, password: Password) -> User:
        user = await self.repository.login(email, password)
        return user
