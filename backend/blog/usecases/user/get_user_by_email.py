from blog.domain.entities.user import User
from blog.domain.repositories.user_repository import UserRepository
from blog.domain.value_objects.email_vo import Email

class GetUserByEmailUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, email: Email) -> User:
        user = self.repository.get_by_email(email)
        if not user:
            raise ValueError("User not found")
        return user