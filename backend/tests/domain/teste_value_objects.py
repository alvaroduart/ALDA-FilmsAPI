import pytest
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password

def test_valid_email():
    email = Email("john.doe@example.com")
    assert email.value() == "john.doe@example.com"

def test_invalid_email():
    with pytest.raises(ValueError):
        Email("invalid-email")

def test_valid_password():
    password = Password("securePassword123")
    assert password.value() == "securePassword123"  

def test_invalid_password():
    with pytest.raises(ValueError):
        Password("short")  # Deve falhar, pois a senha é muito curta    

def test_password_equality():
    password1 = Password("securePassword123")
    password2 = Password("securePassword123")
    assert password1 == password2

def test_password_inequality():
    password1 = Password("securePassword123")
    password2 = Password("differentPassword456")
    assert password1 != password2   

def test_email_equality():
    email1 = Email("john.doe@example.com")
    email2 = Email("john.doe@example.com")
    assert email1 == email2

def test_email_inequality():
    email1 = Email("john.doe@example.com")
    email2 = Email("jane.doe@example.com")
    assert email1 != email2

def test_email_str():
    email = Email("john.doe@example.com")
    assert str(email) == "john.doe@example.com"

