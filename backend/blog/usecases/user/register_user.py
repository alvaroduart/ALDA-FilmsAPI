from blog.domain.entities.user import User
from blog.domain.repositories.user_repository import UserRepository
from fastapi import HTTPException, status


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user: User) -> User:
        # Verifica e-mail já cadastrado

        await self.repository.create(user)
        return user
