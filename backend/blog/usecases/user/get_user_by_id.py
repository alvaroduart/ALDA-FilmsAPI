from blog.domain.entities.user import User
from blog.domain.repositories.user_repository import UserRepository


class GetUserByIdUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_id: str) -> User:
        return self.repository.get_by_id(user_id)

