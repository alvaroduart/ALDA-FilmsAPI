from abc import ABC, abstractmethod
from blog.domain.entities.contact import Contact

class ContactRepository(ABC):
    @abstractmethod
    async def create_contact(self, contact: Contact) -> Contact:        
        pass