import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from blog.domain.entities.contact import Contact
import uuid
from datetime import datetime
from blog.infra.database import Base

class ContactModel(Base):
    __tablename__ = "contacts"

    id: Mapped[str] = mapped_column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    message: Mapped[str] = mapped_column(sa.Text, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(sa.DateTime, default=datetime.utcnow)

    def to_entity(self) -> Contact:
        return Contact(
            id=self.id,
            name=self.name,
            email=self.email,
            message=self.message,
            createdAt=self.createdAt
        )

    @classmethod
    def from_entity(cls, contact: Contact) -> "ContactModel":
        return cls(
            id=contact.id,
            name=contact.name,
            email=contact.email,
            message=contact.message,
            createdAt=contact.createdAt
        )
