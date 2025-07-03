from blog.domain.repositories.user_repository import UserRepository
from blog.domain.entities.user import User
from typing import Optional


class GetCurrentUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: str) -> Optional[User]:
        user = await self.repository.get_current_user(user_id)
        if not user:
            raise ValueError("User not found")
        return user
