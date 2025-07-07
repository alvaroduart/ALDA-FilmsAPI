from blog.domain.entities.contact import Contact
from blog.domain.repositories.contact_repository import ContactRepository

class CreateContactUseCase:
    def __init__(self, repository: ContactRepository):
        self.repository = repository

    def execute(self, contact: Contact) -> None:
        self.repository.create_contact(contact)