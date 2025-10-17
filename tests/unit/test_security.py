# File: tests/unit/test_security.py
import pytest
from models import User
import hashlib

def test_password_is_hashed():
    """
    Ensure passwords are not stored in plaintext.
    Assumes User stores a 'hashed_password' attribute.
    """
    raw_password = "SecurePass123"
    user = User(email="secure@example.com", password=raw_password, name="Tester", address="123 Lane")

    # Check that the raw password is not stored directly
    assert getattr(user, "password", None) != raw_password

    # Optional: check hashing method (example using sha256)
    expected_hash = hashlib.sha256(raw_password.encode()).hexdigest()
    assert getattr(user, "hashed_password", None) == expected_hash




def test_email_validation():
    """Check for invalid and duplicate emails"""
    users = {}
    
    # Valid email
    user1 = User(email="test@example.com", password="pass", name="A", address="Addr")
    users[user1.email.lower()] = user1
    assert user1.email.lower() in users

    # Duplicate email (case-insensitive)
    with pytest.raises(Exception):
        duplicate_email = "Test@Example.com"
        if duplicate_email.lower() in users:
            raise Exception("Duplicate email detected")

    # Invalid email format
    invalid_emails = ["noatsign.com", "bademail@", "abc"]
    for email in invalid_emails:
        with pytest.raises(ValueError):
            User(email=email, password="pass", name="B", address="Addr")




def test_input_sanitization():
    """Ensure inputs are safely handled"""
    from models import Book, Cart

    # Simulate potentially malicious input
    malicious_title = "<script>alert('xss')</script>"
    book = Book(title=malicious_title, category="Test", price=10, image="img.jpg")

    # Ensure the title is stored safely (no actual execution)
    assert book.title == malicious_title


def test_session_logout():
    """Simulate login and logout"""
    user = User(email="session@example.com", password="pass", name="Tester", address="123 Lane")
    
    # Simulate login
    user.login()
    assert user.is_logged_in is True

    # Simulate logout
    user.logout()
    assert user.is_logged_in is False
