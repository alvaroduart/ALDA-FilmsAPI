from blog.domain.entities.contact import Contact
from blog.domain.repositories.contact_repository import ContactRepository

class InMemoryContactRepository(ContactRepository):
    def __init__(self):
        self.contacts = {}

    def create_contact(self, contact):
        return super().create_contact(contact)