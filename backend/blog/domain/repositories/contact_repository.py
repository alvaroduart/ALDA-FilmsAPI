from abc import ABC, abstractmethod
from blog.domain.entities.contact import Contact

class ContactRepository(ABC):
    @abstractmethod
    def create_contact(self, contact: Contact) -> None:        
        pass