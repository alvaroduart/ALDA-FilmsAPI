from datetime import datetime
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password
from typing import Optional


class User:
    def __init__(self, id: str, name: str, email: Email, password: Password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
