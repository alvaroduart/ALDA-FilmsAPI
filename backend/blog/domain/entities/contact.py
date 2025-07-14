from datetime import datetime
from typing import Optional


class Contact:
    def __init__(
        self,
        id: str,
        name: str,
        email: str,
        message: str,
        createdAt: Optional[datetime] = None,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.message = message
        self.createdAt = createdAt if createdAt is not None else datetime.now()
