from blog.domain.entities.user import User
from blog.domain.repositories.user_repository import UserRepository
from blog.domain.value_objects.email_vo import Email

class GetUserByEmailUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, email: Email) -> User:
        user = await self.repository.get_by_email(email)
        if not user:
            raise ValueError("Usuário não encontrado com este e-mail.")
        return user