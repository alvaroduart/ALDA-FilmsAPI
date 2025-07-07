from abc import ABC, abstractmethod
from blog.domain.entities.user import User
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password

class UserRepository(ABC):
    
    @abstractmethod
    def get_by_id(self, user_id: str) -> User:
        pass

    @abstractmethod
    def create(self, user: User) -> None:
        pass
    
    @abstractmethod
    def login(self, email: Email, password: Password) -> User:
        pass
    @abstractmethod
    def logout(self, user_id: str) -> None:
        pass        

    @abstractmethod
    def forgot_password(self, email: Email) -> None:
        pass
 