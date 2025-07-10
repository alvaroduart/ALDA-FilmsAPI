from blog.domain.entities.user import User
from blog.domain.repositories.user_repository import UserRepository
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user: User) -> User:        
        try:
            existing_user = self.repository.get_by_email(user.email)
            if existing_user:
                raise ValueError("Email already exists")
        except:
            pass         
        self.repository.create(user)
        return user

