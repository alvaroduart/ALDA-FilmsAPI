from blog.domain.entities.user import User
from blog.domain.repositories.user_repository import UserRepository


class LogoutUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_id: str) -> None:        
        self.repository.logout(user_id)
