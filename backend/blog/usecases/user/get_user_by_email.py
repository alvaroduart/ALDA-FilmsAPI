from blog.domain.entities.user import User
from blog.domain.repositories.user_repository import UserRepository
from fastapi import HTTPException, status


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user: User) -> User:
        existing_email = await self.repository.get_by_email(user.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já cadastrado."
            )

        existing_name = await self.repository.get_by_username(user.name)
        if existing_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome de usuário já cadastrado.",
            )

        await self.repository.create(user)
        return user
